from django.shortcuts import render
from .models import RFP
from .ai_utils import extract_rfp_structure
from django.shortcuts import render, redirect
from .models import RFP, Vendor  # <-- Added Vendor
from django.core.mail import send_mail
from django.conf import settings
from .models import Proposal # Added Proposal
from .ai_utils import parse_vendor_response # Added the new AI function

def home(request):
    """The Homepage: Shows a list of all RFPs."""
    rfps = RFP.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'rfps': rfps})

def create_rfp(request):
    """The Creation Page: Handles the AI generation."""
    if request.method == "POST":
        # 1. Get the raw text from the user's input box
        user_text = request.POST.get('user_input')
        
        # 2. Send it to Gemini 2.0
        ai_data = extract_rfp_structure(user_text)
        
        # 3. Save to MongoDB
        new_rfp = RFP(
            original_prompt=user_text,
            structured_data=ai_data
        )
        new_rfp.save()
        
        # 4. Show the result
        return render(request, 'core/rfp_result.html', {'rfp': new_rfp})

    # If it's just a GET request, show the empty form
    return render(request, 'core/rfp_create.html')

def vendor_list(request):
    """Shows all vendors and a form to add a new one."""
    if request.method == "POST":
        # Save the new vendor
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('description')
        
        Vendor(name=name, email=email, description=desc).save()
        return redirect('vendor_list')

    # Get all vendors from MongoDB
    vendors = Vendor.objects.all()
    return render(request, 'core/vendor_list.html', {'vendors': vendors})


def send_rfp(request, rfp_id):
    """
    1. GET: Shows a list of vendors to choose from.
    2. POST: Sends the email to selected vendors.
    """
    # Get the specific RFP we are talking about
    rfp = RFP.objects.get(id=rfp_id)
    
    if request.method == "POST":
        # 1. Get the list of vendor IDs the user checked
        selected_vendor_ids = request.POST.getlist('vendors')
        
        # 2. Loop through them and send emails
        vendors = Vendor.objects.filter(id__in=selected_vendor_ids)
        
        for vendor in vendors:
            print(f"📧 Sending email to {vendor.email}...")
            
            subject = f"RFP Request: {rfp.structured_data.get('title', 'Procurement Request')}"
            message = f"""
            Dear {vendor.name},
            
            We are looking to procure the following items:
            {rfp.original_prompt}
            
            Please submit your proposal by {rfp.structured_data.get('timeline_days', 30)} days.
            
            Sincerely,
            Procurement Team
            """
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER, # From Email
                [vendor.email],           # To Email
                fail_silently=False,
            )
        
        # 3. Update status and go home
        rfp.status = 'sent'
        rfp.save()
        return redirect('home')

    # If GET request, show the selection page
    vendors = Vendor.objects.all()
    return render(request, 'core/rfp_send.html', {'rfp': rfp, 'vendors': vendors})


def add_proposal(request, rfp_id):
    rfp = RFP.objects.get(id=rfp_id)
    vendors = Vendor.objects.all()
    
    if request.method == "POST":
        vendor_id = request.POST.get('vendor_id')
        raw_email = request.POST.get('email_text')
        
        # 1. Ask AI to read the email
        ai_data = parse_vendor_response(raw_email)
        
        # 2. Save the result
        vendor = Vendor.objects.get(id=vendor_id)
        Proposal(
            rfp=rfp,
            vendor=vendor,
            raw_response=raw_email,
            parsed_data=ai_data,
            ai_score=ai_data.get('score', 0),
            ai_rationale=ai_data.get('rationale', '')
        ).save()
        
        return redirect('home')

    return render(request, 'core/proposal_add.html', {'rfp': rfp, 'vendors': vendors})

def view_proposals(request, rfp_id):
    """
    Fetches all proposals for a specific RFP and shows them side-by-side.
    """
    rfp = RFP.objects.get(id=rfp_id)
    proposals = Proposal.objects.filter(rfp=rfp).order_by('-ai_score') # Best score first
    
    return render(request, 'core/rfp_compare.html', {'rfp': rfp, 'proposals': proposals})