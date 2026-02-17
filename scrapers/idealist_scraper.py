import requests
from bs4 import BeautifulSoup
import time

class IdealistScraper:
    def __init__(self):
        self.base_url = "https://www.idealist.org"
    
    def search_jobs(self, keyword="intern", location="", max_results=50):
        """Search Idealist for nonprofit internships"""
        jobs = []
        
        try:
            print(f"    Searching Idealist for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            search_url = f"{self.base_url}/en/internships"
            
            params = {
                'q': keyword,
                'location': location
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                job_cards = soup.find_all('div', class_='listing-item')
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('h3')
                        org_elem = card.find('div', class_='organization')
                        location_elem = card.find('div', class_='location')
                        link_elem = card.find('a')
                        
                        if title_elem:
                            title = title_elem.text.strip()
                            company = org_elem.text.strip() if org_elem else 'Unknown'
                            job_location = location_elem.text.strip() if location_elem else 'Various'
                            job_url = link_elem.get('href', '') if link_elem else ''
                            
                            if job_url and not job_url.startswith('http'):
                                job_url = self.base_url + job_url
                            
                            job_id = job_url.split('/')[-1] if job_url else str(int(time.time()))
                            
                            job = {
                                'job_id': f"idealist_{job_id}",
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'url': job_url,
                                'source': 'Idealist'
                            }
                            
                            jobs.append(job)
                            print(f"      ✓ {title[:40]} at {company}")
                    
                    except Exception as e:
                        continue
                
                print(f"    Found {len(jobs)} jobs on Idealist")
        
        except Exception as e:
            print(f"    ❌ Idealist error: {e}")
        
        return jobs