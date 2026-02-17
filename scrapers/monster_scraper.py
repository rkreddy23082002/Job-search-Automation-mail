import requests
from bs4 import BeautifulSoup
import time

class MonsterScraper:
    def __init__(self):
        self.base_url = "https://www.monster.com"
    
    def search_jobs(self, keyword="intern", location="", max_pages=3):
        """Search Monster for internships"""
        jobs = []
        
        try:
            print(f"    Searching Monster for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            for page in range(max_pages):
                search_url = f"{self.base_url}/jobs/search"
                
                params = {
                    'q': keyword,
                    'where': location,
                    'page': page + 1
                }
                
                response = requests.get(search_url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    job_cards = soup.find_all('div', class_='card-content')
                    
                    for card in job_cards:
                        try:
                            title_elem = card.find('h2', class_='title')
                            company_elem = card.find('div', class_='company')
                            location_elem = card.find('div', class_='location')
                            link_elem = card.find('a')
                            
                            if title_elem and company_elem:
                                title = title_elem.text.strip()
                                company = company_elem.text.strip()
                                job_location = location_elem.text.strip() if location_elem else 'Various'
                                job_url = link_elem.get('href', '') if link_elem else ''
                                
                                if job_url and not job_url.startswith('http'):
                                    job_url = self.base_url + job_url
                                
                                job_id = job_url.split('/')[-1] if job_url else str(int(time.time()))
                                
                                if 'intern' in title.lower():
                                    job = {
                                        'job_id': f"monster_{job_id}",
                                        'title': title,
                                        'company': company,
                                        'location': job_location,
                                        'url': job_url,
                                        'source': 'Monster'
                                    }
                                    
                                    jobs.append(job)
                                    print(f"      ✓ {title[:40]} at {company}")
                        
                        except Exception as e:
                            continue
                    
                    time.sleep(2)
            
            print(f"    Found {len(jobs)} jobs on Monster")
        
        except Exception as e:
            print(f"    ❌ Monster error: {e}")
        
        return jobs