import schedule
import time
from scrapers.linkedin_rss_scraper import LinkedInRSSScraper
from database.job_db import JobDatabase  # Same database!
from notifications.email_sender import EmailSender
import config
from datetime import datetime


def run_hourly_job_search():
    """Scrape jobs from LAST HOUR and add to main database"""
    print(f"\n🔥 HOURLY CHECK at {datetime.now().strftime('%I:%M %p')}")
    print("⏰ Searching for jobs posted in LAST HOUR\n")
    
    db = JobDatabase('jobs.db')  # Same database as main.py!
    linkedin_scraper = LinkedInRSSScraper()
    email_sender = EmailSender(config.SENDER_EMAIL, config.SENDER_PASSWORD)
    
    new_jobs_count = 0
    
    print("📊 Scraping LinkedIn (last 1 hour)...")
    try:
        for keyword in config.SEARCH_KEYWORDS:
            # Search last 1 hour only (3600 seconds)
            jobs = linkedin_scraper.search_jobs(keyword, "United States", max_results=50, time_window=3600)
            
            for job in jobs:
                if db.add_job(job):
                    new_jobs_count += 1
                    print(f"  🔥 NEW: {job['title'][:50]} at {job['company']}")
            
            time.sleep(2)
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Send email only if NEW jobs found
    if new_jobs_count > 0:
        print(f"\n📧 Found {new_jobs_count} brand new jobs!")
        # Optional: Send email alert
        # email_sender.send_job_digest(config.RECIPIENT_EMAIL, db.get_last_hour_jobs())
    else:
        print(f"💤 No new jobs this hour")
    
    next_hour = (datetime.now().hour + 1) % 24
    print(f"⏰ Next check at {next_hour:02d}:00\n")


def main():
    print("🔥 HOURLY Job Alert System")
    print("⏰ Runs every hour, adds to MAIN database")
    print("📍 Database: jobs.db (shared with main.py)")
    print("🎯 Time window: Last 1 hour\n")
    
    # Run immediately
    run_hourly_job_search()
    
    # Schedule every hour on the hour
    for hour in range(24):
        schedule.every().day.at(f"{hour:02d}:00").do(run_hourly_job_search)
    
    print("⏰ Scheduled to run every hour")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()