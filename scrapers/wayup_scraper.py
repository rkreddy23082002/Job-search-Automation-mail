import requests
import time

class WayUpScraper:
    def __init__(self):
        self.base_url = "https://www.wayup.com"
    
    def search_jobs(self, keyword="intern", max_results=50):
        """Search WayUp for internships"""
        jobs = []
        
        try:
            print(f"    Searching WayUp for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Accept': 'application/json'
            }
            
            search_url = f"{self.base_url}/api/v3/jobs/search"
            
            params = {
                'query': keyword,
                'type': 'internship',
                'limit': max_results
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_listings = data.get('jobs', [])
                
                print(f"    Found {len(job_listings)} jobs on WayUp")
                
                for job_data in job_listings:
                    title = job_data.get('title', '')
                    company = job_data.get('company', {}).get('name', '')
                    location = job_data.get('location', {}).get('city', 'Various')
                    job_id = job_data.get('id', '')
                    
                    if 'intern' in title.lower():
                        job = {
                            'job_id': f"wayup_{job_id}",
                            'title': title,
                            'company': company,
                            'location': location,
                            'url': f"{self.base_url}/jobs/{job_id}",
                            'source': 'WayUp'
                        }
                        
                        jobs.append(job)
                        print(f"      ✓ {title[:40]} at {company}")
        
        except Exception as e:
            print(f"    ❌ WayUp error: {e}")
        
        return jobs