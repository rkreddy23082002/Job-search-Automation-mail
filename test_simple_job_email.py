from notifications.email_sender import EmailSender
import config

sender = EmailSender(config.SENDER_EMAIL, config.SENDER_PASSWORD)

# Real job data from database
from database.job_db import JobDatabase

db = JobDatabase(config.DB_PATH)
jobs = db.get_todays_jobs()

print(f"Jobs in database: {len(jobs)}")

if jobs:
    print(f"First job: {jobs[0]}")
    print(f"Job tuple length: {len(jobs[0])}")
    
    # Send email with real jobs
    print("\nSending email with real job data...")
    sender.send_job_digest(config.RECIPIENT_EMAIL, jobs[:3])  # Send just first 3 jobs
    print("Done!")
else:
    print("No jobs in database yet!")