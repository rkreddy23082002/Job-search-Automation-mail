from notifications.email_sender import EmailSender
import config

print("Testing email functionality...")
print(f"Sender: {config.SENDER_EMAIL}")
print(f"Recipient: {config.RECIPIENT_EMAIL}")
print(f"Password length: {len(config.SENDER_PASSWORD)} chars")

sender = EmailSender(config.SENDER_EMAIL, config.SENDER_PASSWORD)

# Create a simple test job
test_jobs = [
    (1, 'test_id', 'Test Product Manager Intern', 'Test Company', 
     'Boston, MA', 'https://example.com', 'desc', '2024-02-16', '2024-02-16', 'LinkedIn')
]

print("\nSending test email...")
sender.send_job_digest(config.RECIPIENT_EMAIL, test_jobs)
print("Done! Check your email at godala.r@northeastern.edu")