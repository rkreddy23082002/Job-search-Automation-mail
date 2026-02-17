import schedule
import time
from scrapers.linkedin_hourly_scraper import LinkedInHourlyScraper
from database.job_db_hourly import JobDatabaseHourly
from notifications.email_sender_hourly import EmailSenderHourly
import config


def run_hourly_job_search():
    """Scrape LinkedIn for jobs from LAST HOUR"""
    print(f"\n🔍 Hourly check at {time.strftime('%Y-%m-%d %I:%M %p')}")
    print("⏰ Searching for jobs posted in LAST HOUR\n")
    
    db = JobDatabaseHourly('jobs_hourly.db')
    linkedin_scraper = LinkedInHourlyScraper()
    email_sender = EmailSenderHourly(config.SENDER_EMAIL, config.SENDER_PASSWORD)
    
    new_jobs_count = 0
    
    print("📊 Scraping LinkedIn (last 1 hour)...")
    try:
        for keyword in config.SEARCH_KEYWORDS:
            jobs = linkedin_scraper.search_jobs(keyword, "United States", max_results=50)
            
            for job in jobs:
                if db.add_job(job):
                    new_jobs_count += 1
                    print(f"  🔥 NEW: {job['title'][:50]} at {job['company']}")
            
            time.sleep(2)
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Send email if NEW jobs found
    if new_jobs_count > 0:
        recent_jobs = db.get_recent_jobs()
        print(f"\n📧 HOURLY ALERT: {new_jobs_count} brand new jobs!")
        email_sender.send_hourly_digest(config.RECIPIENT_EMAIL, recent_jobs)
        print(f"✅ Email sent!")
    else:
        print(f"💤 No new jobs this hour")
    
    print(f"⏰ Next check at {time.strftime('%I:00 %p', time.localtime(time.time() + 3600))}\n")


def main():
    print("🔥 HOURLY Job Alert System Started!")
    print("⏰ Checks EVERY HOUR for ultra-fresh jobs")
    print("📍 Source: LinkedIn (last 1 hour)")
    print("🎯 Roles: PM + Data + Design")
    print("🚀 First applicant advantage!\n")
    
    # Run immediately
    run_hourly_job_search()
    
    # Schedule every hour
    schedule.every(1).hours.do(run_hourly_job_search)
    
    print("⏰ Running every hour on the hour")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()