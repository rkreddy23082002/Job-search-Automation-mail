import requests
import time

class WellfoundScraper:
    def __init__(self):
        self.base_url = "https://wellfound.com"
        self.api_url = "https://wellfound.com/api/v1"
    
    def search_jobs(self, keyword="intern", max_results=50):
        """Search Wellfound (AngelList) for startup internships"""
        jobs = []
        
        try:
            print(f"    Searching Wellfound for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Accept': 'application/json'
            }
            
            search_url = f"{self.api_url}/jobs/search"
            
            params = {
                'query': keyword,
                'job_type': 'internship',
                'per_page': max_results
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_listings = data.get('jobs', [])
                
                print(f"    Found {len(job_listings)} jobs on Wellfound")
                
                for job_data in job_listings:
                    title = job_data.get('title', '')
                    company = job_data.get('startup', {}).get('name', '')
                    location = job_data.get('location', 'Remote')
                    job_id = job_data.get('id', '')
                    
                    if 'intern' in title.lower():
                        job = {
                            'job_id': f"wellfound_{job_id}",
                            'title': title,
                            'company': company,
                            'location': location,
                            'url': f"{self.base_url}/l/{job_id}",
                            'source': 'Wellfound'
                        }
                        
                        jobs.append(job)
                        print(f"      ✓ {title[:40]} at {company}")
        
        except Exception as e:
            print(f"    ❌ Wellfound error: {e}")
        
        return jobs