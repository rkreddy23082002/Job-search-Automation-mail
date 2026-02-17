from scrapers.indeed_scraper import IndeedScraper

scraper = IndeedScraper()
print("Testing Indeed scraper...")

jobs = scraper.search_jobs("Program Management Intern", "United States", max_pages=1)

print(f"\n✅ Found {len(jobs)} jobs:")
for job in jobs[:5]:  # Show first 5
    print(f"  - {job['title']} at {job['company']}")
    print(f"    URL: {job['url']}\n")