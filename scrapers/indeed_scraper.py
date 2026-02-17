import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode

class IndeedScraper:
    def __init__(self):
        self.base_url = "https://www.indeed.com/jobs"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    
    def search_jobs(self, keyword, location="United States", max_pages=3):
        """Search Indeed for jobs"""
        jobs = []
        
        for page in range(max_pages):
            params = {
                'q': keyword,
                'l': location,
                'start': page * 10,
                'jt': 'internship',
                'fromage': '7'  # Last 7 days
            }
            
            url = f"{self.base_url}?{urlencode(params)}"
            
            try:
                print(f"    Fetching: {url[:80]}...")
                response = requests.get(url, headers=self.headers, timeout=15)
                print(f"    Status code: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"    ⚠️ Non-200 response")
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple selectors (Indeed changes their HTML frequently)
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                if not job_cards:
                    # Try alternative selector
                    job_cards = soup.find_all('td', class_='resultContent')
                
                print(f"    Found {len(job_cards)} job cards on page")
                
                for card in job_cards:
                    try:
                        # Try to extract job details
                        title_elem = card.find('h2', class_='jobTitle')
                        if not title_elem:
                            title_elem = card.find('a', class_='jcs-JobTitle')
                        
                        company_elem = card.find('span', {'data-testid': 'company-name'})
                        if not company_elem:
                            company_elem = card.find('span', class_='companyName')
                        
                        location_elem = card.find('div', {'data-testid': 'text-location'})
                        if not location_elem:
                            location_elem = card.find('div', class_='companyLocation')
                        
                        if title_elem and company_elem:
                            job_link = title_elem.find('a')
                            if not job_link:
                                job_link = card.find('a', {'data-jk': True})
                            
                            job_id = job_link.get('data-jk', '') if job_link else ''
                            if not job_id:
                                job_id = job_link.get('id', '').replace('job_', '') if job_link else ''
                            
                            job = {
                                'job_id': f"indeed_{job_id}_{int(time.time())}",
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'location': location_elem.text.strip() if location_elem else location,
                                'url': f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else '#',
                                'source': 'Indeed'
                            }
                            
                            # Less strict filter - just check if it's an internship
                            title_lower = job['title'].lower()
                            if 'intern' in title_lower:
                                jobs.append(job)
                                print(f"      ✓ {job['title'][:50]}...")
                    
                    except Exception as e:
                        print(f"      ✗ Error parsing card: {e}")
                        continue
                
                # Be respectful - add delay between pages
                time.sleep(3)
            
            except Exception as e:
                print(f"    ❌ Error scraping Indeed: {e}")
                break
        
        return jobs