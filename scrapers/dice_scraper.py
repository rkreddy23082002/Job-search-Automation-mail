import requests
from bs4 import BeautifulSoup
import time

class DiceScraper:
    def __init__(self):
        self.base_url = "https://www.dice.com"
    
    def search_jobs(self, keyword="intern", location="", max_results=50):
        """Search Dice for tech internships"""
        jobs = []
        
        try:
            print(f"    Searching Dice for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'x-api-key': 'public'
            }
            
            # Dice has an API endpoint
            api_url = f"{self.base_url}/api/v5/search/jobs"
            
            params = {
                'q': keyword,
                'location': location,
                'employmentType': 'INTERN',
                'pageSize': max_results
            }
            
            response = requests.get(api_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_listings = data.get('data', [])
                
                print(f"    Found {len(job_listings)} jobs on Dice")
                
                for job_data in job_listings:
                    title = job_data.get('title', '')
                    company = job_data.get('employer', {}).get('name', '')
                    location_info = job_data.get('location', '')
                    job_id = job_data.get('id', '')
                    
                    if 'intern' in title.lower():
                        job = {
                            'job_id': f"dice_{job_id}",
                            'title': title,
                            'company': company,
                            'location': location_info,
                            'url': f"{self.base_url}/job-detail/{job_id}",
                            'source': 'Dice'
                        }
                        
                        jobs.append(job)
                        print(f"      ✓ {title[:40]} at {company}")
        
        except Exception as e:
            print(f"    ❌ Dice error: {e}")
        
        return jobs