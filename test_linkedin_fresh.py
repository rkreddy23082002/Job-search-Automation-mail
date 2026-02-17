from scrapers.linkedin_rss_scraper import LinkedInRSSScraper

scraper = LinkedInRSSScraper()

print("Testing LinkedIn with different date filters...\n")

# Test 1: No date filter
print("=" * 50)
print("Test 1: WITHOUT 24hr filter")
print("=" * 50)
jobs_no_filter = scraper.search_jobs("Product Management Intern", "United States", max_results=10)
print(f"Found {len(jobs_no_filter)} jobs\n")

# Now manually test with the 24hr filter URL
import requests
from bs4 import BeautifulSoup

print("=" * 50)
print("Test 2: WITH 24hr filter (f_TPR=r86400)")
print("=" * 50)

url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Product%20Management%20Intern&location=United%20States&f_JT=I&f_TPR=r86400"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
job_cards = soup.find_all('div', class_='base-card')

print(f"Found {len(job_cards)} jobs with 24hr filter")

for card in job_cards[:5]:
    try:
        title = card.find('h3', class_='base-search-card__title').text.strip()
        company = card.find('h4', class_='base-search-card__subtitle').text.strip()
        print(f"  - {title} at {company}")
    except:
        pass

print("\n" + "=" * 50)
print("If Test 2 shows 0 jobs, LinkedIn's 24hr filter isn't working")
print("=" * 50)