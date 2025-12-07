AI-Powered RFP Management System

An intelligent procurement agent that streamlines the Request for Proposal (RFP) lifecycle. This application replaces manual email workflows with an AI-assisted dashboard, allowing users to create RFPs using natural language, manage vendors, automate email communication, and use GenAI (Gemini 2.0) to parse messy vendor responses into structured comparison tables.

🚀 Features

AI-Driven RFP Creation: Converts natural language (e.g., "I need 20 laptops for the design team...") into structured JSON data (Items, Budget, Timeline) using Google Gemini.

Automated Vendor Communication: Manages vendor lists and dispatches professional RFP emails via SMTP integration.

Intelligent Response Parsing: Users can paste unstructured vendor email replies, and the system uses AI to automatically extract pricing, warranty terms, and delivery dates.

Smart Comparison Matrix: Auto-generates a side-by-side comparison table with AI-generated scores (0-100) and rationales to help the user select the best offer.

🛠 Tech Stack

I chose a Python-centric stack to leverage native AI integration and rapid prototyping capabilities:

Backend: Django 5.0 (Python) - Selected for its "batteries-included" architecture and seamless integration with AI SDKs, replacing the need for complex Node.js middleware.

Database: MongoDB Atlas (Cloud) - Chosen for its document model, which is perfect for storing unstructured RFP requirements and varying vendor response formats.

AI Engine: Google Gemini 2.0 Flash - Selected for its low latency and superior ability to output strict JSON schemas.

ORM: MongoEngine - Used to bridge Django's object-oriented structure with MongoDB.

Frontend: Django Templates with a custom CSS dashboard design.

⚙️ Setup Instructions

1. Prerequisites

Python 3.10 or higher

A MongoDB Atlas Account (Free Tier)

A Google Gemini API Key (AI Studio)

2. Installation

# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/ai-rfp-manager.git](https://github.com/YOUR_USERNAME/ai-rfp-manager.git)
cd ai-rfp-manager

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install django python-dotenv pymongo[srv] mongoengine google-generativeai


3. Configuration

Create a .env file in the root directory (next to manage.py) with the following secrets:

MONGO_URI="mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/?retryWrites=true&w=majority"
GEMINI_API_KEY="AIzaSy...Your_Key_Here"


4. Running the Application

python manage.py runserver 8080


Open your browser and navigate to: http://127.0.0.1:8080.

📚 API & URL Structure

Method

Endpoint

Description

GET

/

Dashboard: Lists all RFPs, dates, and current status.

POST

/create/

Create RFP: Sends user prompt to Gemini → Saves structured RFP object.

GET

/vendors/

Vendor Manager: Lists existing vendors.

POST

/vendors/

Add Vendor: Saves a new vendor to the MongoDB collection.

POST

/rfp/<id>/send/

Emailer: Triggers SMTP dispatch to selected vendors.

POST

/rfp/<id>/add-proposal/

Parser: Sends raw vendor email text to Gemini → Saves structured Proposal object.

GET

/rfp/<id>/compare/

Comparison: Renders the side-by-side evaluation matrix.

🧠 Design Decisions & Assumptions

Why Django instead of Node.js?

While the assignment suggested Node.js, I opted for Django because Python is the primary language for AI engineering. Using Django allowed me to call the Gemini SDK directly within the view logic, reducing architectural complexity. It also allowed for faster backend scaffolding using Django's template system.

Database Choice

Procurement data is highly variable. A rigid SQL schema would struggle with RFPs that sometimes require "Technical Specs" and other times require "Fabric Dimensions." MongoDB allows the structured_data field to store whatever JSON the AI extracts without requiring schema migrations.

Key Assumptions

Single User Mode: As per the "Non-Goals" section of the assignment, no user authentication system was implemented.

Email Simulation: The application is currently configured to use Django's ConsoleBackend. This means emails are printed to the terminal window to prove functionality without spamming real email addresses during the review process.

AI Rate Limits: The system assumes standard Gemini API rate limits. In a production environment, a queue system (like Celery) would be added to handle high traffic.

🤖 AI Tools Usage

Google Gemini 2.0 Flash: The core intelligence engine. I used it for two distinct tasks:

Extraction: Converting natural language prompts into a strict JSON schema for the database.

Reasoning: Analyzing vendor proposals to assign a "Value Score" (0-100) based on price and timeline.

Prompt Engineering: I utilized "System Instructions" in the prompt to strictly forbid Markdown formatting (```json) in the response, ensuring the application code can parse the output reliably.