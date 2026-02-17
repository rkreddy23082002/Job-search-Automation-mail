import schedule
import time
from scrapers.linkedin_rss_scraper import LinkedInRSSScraper
from database.job_db import JobDatabase
from notifications.email_sender import EmailSender
import config


def run_job_search():
    """Scrape LinkedIn for FRESH internships from last 24 hours"""
    print(f"\n🔍 Starting job search at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("📅 Searching LinkedIn for jobs from LAST 24 HOURS\n")
    
    db = JobDatabase(config.DB_PATH)
    linkedin_scraper = LinkedInRSSScraper()
    email_sender = EmailSender(config.SENDER_EMAIL, config.SENDER_PASSWORD)
    
    new_jobs_count = 0
    
    print("📊 Scraping LinkedIn (last 24 hours only)...")
    try:
        for keyword in config.SEARCH_KEYWORDS:
            jobs = linkedin_scraper.search_jobs(keyword, "United States", max_results=50)
            
            for job in jobs:
                if db.add_job(job):
                    new_jobs_count += 1
                    print(f"  ✅ New: {job['title'][:50]} at {job['company']}")
            
            time.sleep(3)
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Send email
    if new_jobs_count > 0:
        todays_jobs = db.get_todays_jobs()
        print(f"\n📧 Sending email with {new_jobs_count} FRESH jobs (all <24hrs old)...")
        email_sender.send_job_digest(config.RECIPIENT_EMAIL, todays_jobs)
        print(f"✅ Email sent!")
    else:
        print(f"\n💤 No new jobs from last 24 hours")
    
    print(f"\n✨ Found {new_jobs_count} fresh jobs!\n")


def main():
    print("🚀 Job Alert System - LinkedIn Only")
    print("📅 Filter: Last 24 hours (GUARANTEED FRESH)")
    print("🎯 Roles: PM/Product + Data/Analytics + UX/UI Design\n")
    
    run_job_search()
    
    # Schedule daily
    schedule.every().day.at(config.EMAIL_TIME).do(run_job_search)
    
    print(f"⏰ Scheduled to run daily at {config.EMAIL_TIME}")
    print("Press Ctrl+C to stop or run manually anytime!\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()