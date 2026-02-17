import requests
from bs4 import BeautifulSoup
import time

class ZipRecruiterScraper:
    def __init__(self):
        self.base_url = "https://www.ziprecruiter.com"
    
    def search_jobs(self, keyword="intern", location="United States", max_pages=3):
        """Search ZipRecruiter for internships"""
        jobs = []
        
        try:
            print(f"    Searching ZipRecruiter for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            for page in range(1, max_pages + 1):
                search_url = f"{self.base_url}/jobs-search"
                
                params = {
                    'search': keyword,
                    'location': location,
                    'page': page
                }
                
                response = requests.get(search_url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find job cards
                    job_cards = soup.find_all('div', class_='job_content')
                    
                    for card in job_cards:
                        try:
                            title_elem = card.find('h2', class_='title')
                            company_elem = card.find('a', class_='company_name')
                            location_elem = card.find('li', class_='location')
                            link_elem = card.find('a', class_='job_link')
                            
                            if title_elem and company_elem:
                                title = title_elem.text.strip()
                                company = company_elem.text.strip()
                                job_location = location_elem.text.strip() if location_elem else location
                                job_url = link_elem.get('href', '') if link_elem else ''
                                
                                if not job_url.startswith('http'):
                                    job_url = self.base_url + job_url
                                
                                job_id = job_url.split('/')[-1] if job_url else str(int(time.time()))
                                
                                if 'intern' in title.lower():
                                    job = {
                                        'job_id': f"ziprecruiter_{job_id}",
                                        'title': title,
                                        'company': company,
                                        'location': job_location,
                                        'url': job_url,
                                        'source': 'ZipRecruiter'
                                    }
                                    
                                    jobs.append(job)
                                    print(f"      ✓ {title[:40]} at {company}")
                        
                        except Exception as e:
                            continue
                    
                    time.sleep(2)  # Be respectful
                
                else:
                    print(f"    Status: {response.status_code}")
                    break
            
            print(f"    Found {len(jobs)} jobs on ZipRecruiter")
        
        except Exception as e:
            print(f"    ❌ ZipRecruiter error: {e}")
        
        return jobs