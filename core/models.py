from django.db import models
from mongoengine import ReferenceField, CASCADE, IntField # Added ReferenceField, CASCADE, IntField

# Create your models here.
from mongoengine import Document, StringField, FloatField, ListField, DictField, DateTimeField
import datetime

# 1. THE VENDOR MODEL
# This stores the people we will email.
class Vendor(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True)
    description = StringField()  # e.g., "Electronics Supplier"
    
    def __str__(self):
        return self.name

# 2. THE RFP MODEL
# This is the main object of your assignment.
class RFP(Document):
    # The original text the user typed (e.g., "I need 20 laptops...")
    original_prompt = StringField(required=True)
    
    # The structured data AI extracts (Budget, Items, Due Date)
    # We use DictField because the structure might vary
    structured_data = DictField()
    
    # Status: 'draft', 'sent', 'closed'
    status = StringField(default='draft')
    
    # When was this created?
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    # We will verify this works later!
    def __str__(self):
        return f"RFP created on {self.created_at.date()}"
    

# 3. THE PROPOSAL MODEL
# Stores the parsed response from a vendor
class Proposal(Document):
    rfp = ReferenceField(RFP, reverse_delete_rule=CASCADE) # Link to the specific RFP
    vendor = ReferenceField(Vendor)                        # Link to the Vendor who sent it
    
    raw_response = StringField() # The full email text
    parsed_data = DictField()    # AI extracted data (Price, Timeline, etc.)
    
    ai_score = IntField(default=0)       # We will ask AI to rate the offer (0-100)
    ai_rationale = StringField()         # Why did AI give this score?
    
    created_at = DateTimeField(default=datetime.datetime.utcnow)