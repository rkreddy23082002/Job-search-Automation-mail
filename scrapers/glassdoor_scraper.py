import requests
from bs4 import BeautifulSoup
import time

class GlassdoorScraper:
    def __init__(self):
        self.base_url = "https://www.glassdoor.com"
    
    def search_jobs(self, keyword="intern", location="United States", max_results=50):
        """Search Glassdoor for internships"""
        jobs = []
        
        try:
            print(f"    Searching Glassdoor for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml'
            }
            
            search_url = f"{self.base_url}/Job/jobs.htm"
            
            params = {
                'sc.keyword': keyword,
                'locT': 'N',
                'locId': '1',
                'jobType': 'intern'
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Glassdoor uses React, so we look for job data in scripts
                job_cards = soup.find_all('li', class_='react-job-listing')
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('a', class_='jobLink')
                        company_elem = card.find('div', class_='jobHeader')
                        
                        if title_elem:
                            title = title_elem.text.strip()
                            job_url = self.base_url + title_elem.get('href', '')
                            job_id = title_elem.get('data-id', str(int(time.time())))
                            
                            company = company_elem.text.strip() if company_elem else 'Unknown'
                            
                            if 'intern' in title.lower():
                                job = {
                                    'job_id': f"glassdoor_{job_id}",
                                    'title': title,
                                    'company': company,
                                    'location': location,
                                    'url': job_url,
                                    'source': 'Glassdoor'
                                }
                                
                                jobs.append(job)
                                print(f"      ✓ {title[:40]} at {company}")
                    
                    except Exception as e:
                        continue
                
                print(f"    Found {len(jobs)} jobs on Glassdoor")
        
        except Exception as e:
            print(f"    ❌ Glassdoor error: {e}")
        
        return jobs