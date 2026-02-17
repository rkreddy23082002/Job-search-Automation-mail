import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSenderHourly:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_hourly_digest(self, recipient_email, jobs):
        """Send hourly alert email"""
        
        if not jobs:
            return
        
        print(f"  📧 Preparing HOURLY alert...")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🔥 {len(jobs)} BRAND NEW Jobs (Last Hour) - {datetime.now().strftime('%I:%M %p')}"
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        
        html_body = self._create_html_email(jobs)
        msg.attach(MIMEText(html_body, 'html'))
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"  ✅ Hourly alert sent!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    def _create_html_email(self, jobs):
        """Create HTML for hourly alert"""
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #FF4500; color: white; padding: 20px; text-align: center; }}
                .job-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; background: #fff9e6; }}
                .job-title {{ font-size: 18px; font-weight: bold; color: #FF4500; }}
                .company {{ font-size: 16px; color: #333; }}
                .apply-btn {{ background-color: #FF4500; color: white; padding: 10px 20px; 
                             text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔥 BRAND NEW JOBS - POSTED IN LAST HOUR!</h1>
                <p>{datetime.now().strftime('%I:%M %p, %B %d, %Y')}</p>
            </div>
            
            <div style="padding: 20px;">
                <p><strong>⚡ ULTRA FRESH: {len(jobs)} jobs posted in the last 60 minutes!</strong></p>
                <p>Apply NOW - be one of the first applicants! 🚀</p>
        """
        
        for job in jobs:
            html += f"""
            <div class="job-card">
                <div class="job-title">🔥 {job[2]}</div>
                <div class="company">🏢 {job[3]}</div>
                <div class="location">📍 {job[4]}</div>
                <div style="margin-top: 5px; color: #888; font-size: 13px;">Posted: Last hour ⏰</div>
                <a href="{job[5]}" class="apply-btn">Apply NOW →</a>
            </div>
            """
        
        html += """
            </div>
            <div style="text-align: center; padding: 20px; color: #888; font-size: 12px;">
                <p>🔥 Hourly Job Alert System - You're getting jobs MINUTES after they're posted!</p>
            </div>
        </body>
        </html>
        """
        
        return html