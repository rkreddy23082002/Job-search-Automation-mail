import requests
from bs4 import BeautifulSoup
import time

class CheggScraper:
    def __init__(self):
        self.base_url = "https://www.internships.com"
    
    def search_jobs(self, keyword="intern", location="", max_pages=3):
        """Search Chegg Internships"""
        jobs = []
        
        try:
            print(f"    Searching Chegg Internships for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            for page in range(1, max_pages + 1):
                search_url = f"{self.base_url}/search"
                
                params = {
                    'keywords': keyword,
                    'location': location,
                    'page': page
                }
                
                response = requests.get(search_url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    job_cards = soup.find_all('div', class_='listing')
                    
                    for card in job_cards:
                        try:
                            title_elem = card.find('h2', class_='listing-title')
                            company_elem = card.find('div', class_='company')
                            location_elem = card.find('div', class_='location')
                            link_elem = card.find('a', class_='listing-link')
                            
                            if title_elem:
                                title = title_elem.text.strip()
                                company = company_elem.text.strip() if company_elem else 'Unknown'
                                job_location = location_elem.text.strip() if location_elem else 'Various'
                                job_url = link_elem.get('href', '') if link_elem else ''
                                
                                if job_url and not job_url.startswith('http'):
                                    job_url = self.base_url + job_url
                                
                                job_id = job_url.split('/')[-1] if job_url else str(int(time.time()))
                                
                                job = {
                                    'job_id': f"chegg_{job_id}",
                                    'title': title,
                                    'company': company,
                                    'location': job_location,
                                    'url': job_url,
                                    'source': 'Chegg'
                                }
                                
                                jobs.append(job)
                                print(f"      ✓ {title[:40]} at {company}")
                        
                        except Exception as e:
                            continue
                    
                    time.sleep(2)
            
            print(f"    Found {len(jobs)} jobs on Chegg Internships")
        
        except Exception as e:
            print(f"    ❌ Chegg error: {e}")
        
        return jobs