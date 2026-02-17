import requests
import time

class SimplifyScraper:
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/.github/scripts/listings.json"
    
    def search_jobs(self):
        """Scrape Simplify - Filter for PM/Data/Design roles ONLY"""
        jobs = []
        
        try:
            print("📊 Scraping Simplify.jobs (aggregates 100+ sites)...")
            
            response = requests.get(self.base_url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"    Found {len(data)} total postings, filtering for YOUR roles...")
                
                # YOUR TARGET ROLES - Must match at least ONE
                target_roles = [
                    # Product/Program Management
                    'product manager', 'product management', 'product intern',
                    'program manager', 'program management',
                    'project manager', 'project management',
                    'technical product', 'tpm', 'apm', 'associate product',
                    'strategy', 'product analyst', 'product owner',
                    
                    # Data/Analytics
                    'data analyst', 'data science', 'data scientist',
                    'business analyst', 'business intelligence', 'bi analyst',
                    'analytics', 'quantitative', 'insights analyst',
                    
                    # Design
                    'ux design', 'ui design', 'ux/ui', 'ux designer', 'ui designer',
                    'user experience', 'user interface',
                    'product design', 'product designer',
                    'ux research', 'ux researcher', 'interaction design'
                ]
                
                # EXCLUDE THESE
                exclude_roles = [
                    'software engineer', 'software developer', 'sde', 'swe',
                    'backend engineer', 'frontend engineer', 'full stack',
                    'devops', 'cloud engineer', 'data engineer',
                    'ml engineer', 'machine learning engineer',
                    'hardware', 'mechanical', 'electrical', 'civil',
                    'firmware', 'qa engineer', 'test engineer',
                    'manufacturing', 'supply chain', 'sales intern',
                    'marketing intern', 'hr intern', 'human resources intern',
                    'finance intern', 'accounting intern'
                ]
                
                for job_data in data:
                    company = job_data.get('company_name', '')
                    title = job_data.get('title', '')
                    locations = job_data.get('locations', ['Various'])
                    url_link = job_data.get('url', '')
                    is_active = job_data.get('active', True)
                    
                    if not is_active or not company or not title:
                        continue
                    
                    title_lower = title.lower()
                    
                    # Must be intern or co-op
                    if not ('intern' in title_lower or 'co-op' in title_lower or 'co op' in title_lower):
                        continue
                    
                    # Must match at least ONE target role
                    has_target = any(role in title_lower for role in target_roles)
                    if not has_target:
                        continue
                    
                    # Must NOT be in exclude list
                    has_exclude = any(exclude in title_lower for exclude in exclude_roles)
                    if has_exclude:
                        continue
                    
                    # Passed all filters!
                    job = {
                        'job_id': f"simplify_{company.replace(' ', '_')}_{title[:30].replace(' ', '_')}",
                        'title': title,
                        'company': company,
                        'location': locations[0] if locations else 'Various',
                        'url': url_link,
                        'source': 'Simplify'
                    }
                    
                    jobs.append(job)
                    
                    # Show first 10
                    if len(jobs) <= 10:
                        print(f"      ✓ {title[:50]} at {company}")
                
                if len(jobs) > 10:
                    print(f"      ... and {len(jobs) - 10} more")
                
                print(f"    ✅ Filtered to {len(jobs)} relevant PM/Data/Design roles from {len(data)} total")
        
        except Exception as e:
            print(f"    ❌ Simplify error: {e}")
        
        return jobs