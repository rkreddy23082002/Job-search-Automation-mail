import requests
import time

class LevelsFyiScraper:
    def __init__(self):
        self.base_url = "https://www.levels.fyi/internships"
    
    def search_jobs(self, max_results=50):
        """Scrape Levels.fyi internship listings"""
        jobs = []
        
        try:
            print(f"    Fetching from Levels.fyi...")
            
            # Levels.fyi has a public API endpoint
            api_url = "https://www.levels.fyi/js/internshipData.json"
            
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for job_data in data[:max_results]:
                    company = job_data.get('company', '')
                    role = job_data.get('title', '')
                    location = job_data.get('location', 'Various')
                    
                    if company and role:
                        job = {
                            'job_id': f"levelsfyi_{company.replace(' ', '_')}_{int(time.time())}",
                            'title': role,
                            'company': company,
                            'location': location,
                            'url': f"https://www.levels.fyi/internships/?search={company.replace(' ', '+')}",
                            'source': 'Levels.fyi'
                        }
                        
                        if 'intern' in role.lower():
                            jobs.append(job)
                            print(f"      ✓ {role[:40]} at {company}")
                
                print(f"    Found {len(jobs)} internships")
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        return jobs