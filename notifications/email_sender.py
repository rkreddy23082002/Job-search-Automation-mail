import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_job_digest(self, recipient_email, jobs):
        """Send formatted email with job listings"""
        
        if not jobs:
            print("  ⚠️  No jobs to send")
            return
        
        print(f"  📧 Preparing email for {recipient_email}")
        print(f"  📊 Jobs to send: {len(jobs)}")
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🎯 {len(jobs)} New Internship Opportunities - {datetime.now().strftime('%B %d, %Y')}"
        msg['From'] = self.sender_email
        # Send to both emails
        msg['To'] = 'godalaramakrishnareddy@gmail.com'
        
        print(f"  📝 Subject: {msg['Subject']}")
        print(f"  📤 From: {self.sender_email}")
        print(f"  📥 To: {recipient_email}")
        
        # Create HTML email body
        try:
            print(f"  🎨 Creating HTML email...")
            html_body = self._create_html_email(jobs)
            print(f"  ✅ HTML created ({len(html_body)} characters)")
            
            msg.attach(MIMEText(html_body, 'html'))
            print(f"  ✅ HTML attached to message")
            
        except Exception as e:
            print(f"  ❌ Error creating HTML: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Send email
        try:
            print(f"  🔌 Connecting to Gmail SMTP...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            
            print(f"  🔒 Starting TLS...")
            server.starttls()
            
            print(f"  🔑 Logging in...")
            server.login(self.sender_email, self.sender_password)
            
            print(f"  📨 Sending email...")
            result = server.send_message(msg)
            
            server.quit()
            
            print(f"  ✅ Email sent successfully!")
            print(f"  📬 Check inbox at: {recipient_email}")
            print(f"  📬 Also check: Spam, Promotions, Updates tabs")
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"  ❌ Authentication failed: {e}")
        except Exception as e:
            print(f"  ❌ Error sending: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_html_email(self, jobs):
        """Create nicely formatted HTML email"""
        
        try:
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ background-color: #0073b1; color: white; padding: 20px; text-align: center; }}
                    .job-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                    .job-title {{ font-size: 18px; font-weight: bold; color: #0073b1; }}
                    .company {{ font-size: 16px; color: #333; }}
                    .location {{ color: #666; font-size: 14px; }}
                    .apply-btn {{ background-color: #0073b1; color: white; padding: 10px 20px; 
                                 text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🎯 Your Daily Internship Digest</h1>
                    <p>{datetime.now().strftime('%A, %B %d, %Y')}</p>
                </div>
                
                <div style="padding: 20px;">
                    <p>Hey Rama! Found <strong>{len(jobs)} new opportunities</strong> posted in the last 24 hours:</p>
            """
            
            # Add each job card
            for i, job in enumerate(jobs):
                try:
                    # Extract job details safely
                    job_id = job[1] if len(job) > 1 else 'unknown'
                    title = str(job[2]) if len(job) > 2 else 'Unknown Title'
                    company = str(job[3]) if len(job) > 3 else 'Unknown Company'
                    location = str(job[4]) if len(job) > 4 else 'Unknown Location'
                    url = str(job[5]) if len(job) > 5 else '#'
                    source = str(job[9]) if len(job) > 9 else 'Unknown Source'
                    
                    # Escape any problematic characters in HTML
                    title = title.replace('<', '&lt;').replace('>', '&gt;')
                    company = company.replace('<', '&lt;').replace('>', '&gt;')
                    
                    html += f"""
                    <div class="job-card">
                        <div class="job-title">{title}</div>
                        <div class="company">🏢 {company}</div>
                        <div class="location">📍 {location}</div>
                        <div style="margin-top: 5px; color: #888; font-size: 13px;">Source: {source}</div>
                        <a href="{url}" class="apply-btn">View Job →</a>
                    </div>
                    """
                    
                except Exception as e:
                    print(f"    ⚠️  Error formatting job {i}: {e}")
                    continue
            
            html += """
                </div>
                <div style="text-align: center; padding: 20px; color: #888; font-size: 12px;">
                    <p>This is an automated digest from your Job Alert System</p>
                    <p>All jobs posted in the last 24 hours ⏰</p>
                </div>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            print(f"  ❌ Error in _create_html_email: {e}")
            import traceback
            traceback.print_exc()
            raise