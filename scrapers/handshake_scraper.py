import requests
import time

class HandshakeScraper:
    def __init__(self):
        self.base_url = "https://app.joinhandshake.com/stu"
        # Note: Handshake requires login, so this is a public endpoint
        self.api_url = "https://app.joinhandshake.com/api/public/postings"
    
    def search_jobs(self, keyword="intern", location="United States"):
        """Search Handshake public postings"""
        jobs = []
        
        try:
            print(f"    Searching Handshake for: {keyword}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Accept': 'application/json'
            }
            
            params = {
                'query': keyword,
                'job_types[]': 'Internship',
                'per_page': 50
            }
            
            response = requests.get(self.api_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                postings = data.get('results', [])
                
                print(f"    Found {len(postings)} jobs on Handshake")
                
                for posting in postings:
                    title = posting.get('title', '')
                    employer = posting.get('employer_name', '')
                    locations = posting.get('location_names', ['Various'])
                    job_id = posting.get('id', '')
                    
                    if 'intern' in title.lower():
                        job = {
                            'job_id': f"handshake_{job_id}",
                            'title': title,
                            'company': employer,
                            'location': locations[0] if locations else 'Various',
                            'url': f"https://app.joinhandshake.com/stu/jobs/{job_id}",
                            'source': 'Handshake'
                        }
                        
                        jobs.append(job)
                        print(f"      ✓ {title[:40]} at {employer}")
            
        except Exception as e:
            print(f"    ❌ Handshake error: {e}")
        
        return jobs