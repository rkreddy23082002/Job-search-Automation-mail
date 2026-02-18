import schedule
import time
from scrapers.linkedin_rss_scraper import LinkedInRSSScraper
from database.job_db import JobDatabase
from notifications.email_sender import EmailSender
import config


def run_job_search():
    """Scrape jobs from LAST 24 HOURS"""
    print(f"\n🔍 DAILY CHECK at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("📅 Searching for jobs from LAST 24 HOURS\n")
    
    db = JobDatabase('jobs.db')
    linkedin_scraper = LinkedInRSSScraper()
    email_sender = EmailSender(config.SENDER_EMAIL, config.SENDER_PASSWORD)
    
    new_jobs_count = 0
    
    print("📊 Scraping LinkedIn (last 24 hours)...")
    try:
        for keyword in config.SEARCH_KEYWORDS:
            # Search last 24 hours (86400 seconds)
            jobs = linkedin_scraper.search_jobs(keyword, "United States", max_results=50, time_window=86400)
            
            for job in jobs:
                if db.add_job(job):
                    new_jobs_count += 1
                    print(f"  ✅ New: {job['title'][:50]} at {job['company']}")
            
            time.sleep(3)
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Send daily email
    if new_jobs_count > 0:
        todays_jobs = db.get_todays_jobs()
        print(f"\n📧 Sending daily digest with {new_jobs_count} jobs...")
        email_sender.send_job_digest(config.RECIPIENT_EMAIL, todays_jobs)
        print(f"✅ Email sent!")
    else:
        print(f"\n💤 No new jobs")
    
    print(f"\n✨ Found {new_jobs_count} jobs\n")


def main():
    print("🚀 DAILY Job Alert System")
    print("📅 Runs at 7 AM daily")
    print("📍 Database: jobs.db (shared with hourly.py)")
    print("🎯 Time window: Last 24 hours\n")
    
    run_job_search()
    
    # Schedule daily at 7 AM
    schedule.every().day.at(config.EMAIL_TIME).do(run_job_search)
    
    print(f"⏰ Scheduled to run daily at {config.EMAIL_TIME}")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()