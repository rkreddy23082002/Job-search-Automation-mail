import os
from dotenv import load_dotenv

load_dotenv()

# Email settings
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# Job search keywords
SEARCH_KEYWORDS = [
    # Product/Program Management
    "Product Manager Intern",
    "Program Manager Intern",
    "Product Management Intern",
    "Program Management Intern",
    "Associate Product Manager",
    "Technical Program Manager Intern",
    
    # Data/Analytics
    "Data Analyst Intern",
    "Business Analyst Intern",
    "Data Science Intern",
    "Business Intelligence Intern",
    "Analytics Intern",
    
    # UX/UI Design - EXPANDED
    "UX Designer Intern",
    "UI Designer Intern",
    "UX Design Intern",
    "UI Design Intern",
    "Product Designer Intern",
    "Product Design Intern",
    "User Experience Intern",
    "User Interface Intern",
    "UX Researcher Intern",
    "UX Research Intern",
    "Design Intern",
    "Visual Designer Intern",
    "Interaction Designer Intern"
]

LOCATIONS = ["United States"]

# Database
DB_PATH = "jobs.db"

# Schedule
EMAIL_TIME = "07:00"