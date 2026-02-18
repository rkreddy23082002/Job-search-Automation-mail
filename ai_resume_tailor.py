import os
from dotenv import load_dotenv

load_dotenv()

class AIResumeTailor:
    def __init__(self):
        # For now, AI is disabled - you'll use Claude chat instead
        self.base_resume = self.load_base_resume()
        print("⚠️  AI tailoring using Claude chat (free mode)")
    
    def load_base_resume(self):
        """Load your master resume"""
        try:
            with open('resume_master.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print("⚠️  resume_master.txt not found - create it later")
            return "Your resume here"
    
    def tailor_resume(self, job_title, job_description, company):
        """Placeholder - use Claude chat for now"""
        return f"Use Claude chat to tailor resume for {job_title} at {company}"
    
    def generate_cover_letter(self, job_title, job_description, company):
        """Placeholder - use Claude chat for now"""
        return f"Use Claude chat to generate cover letter for {job_title} at {company}"