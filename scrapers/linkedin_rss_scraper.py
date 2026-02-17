import requests
from bs4 import BeautifulSoup
import time

class LinkedInRSSScraper:
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    def search_jobs(self, keyword, location="United States", max_results=50):
        """Search LinkedIn - Accept ALL jobs in PM/Data/Design categories"""
        jobs = []
        
        try:
            print(f"    Searching LinkedIn (24hrs): {keyword}...")
            
            # Last 24 hours
            params = f"?keywords={keyword.replace(' ', '%20')}&location={location}&f_JT=I&f_TPR=r86400"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            url = self.base_url + params
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')
                
                print(f"    Found {len(job_cards)} jobs, checking categories...")
                
                for card in job_cards:
                    try:
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        location_elem = card.find('span', class_='job-search-card__location')
                        link_elem = card.find('a', class_='base-card__full-link')
                        
                        if title_elem and company_elem and link_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip()
                            location_text = location_elem.text.strip() if location_elem else location
                            url = link_elem.get('href', '')
                            
                            title_lower = title.lower()
                            
                            # Must be intern/co-op
                            if not ('intern' in title_lower or 'co-op' in title_lower or 'co op' in title_lower):
                                continue
                            
                            # Skip aggregators only
                            if company in ['Lensa', 'Jobs via Dice']:
                                continue
                            
                            # Check if it's in ANY of your 3 categories
                            # Very broad matching - if keyword searched for it, it's relevant
                            
                            # Product/Program keywords (BROAD)
                            pm_keywords = [
                                'product', 'program', 'project',
                                'management', 'manager', 'strategy',
                                'operations', 'analyst', 'owner'
                            ]
                            
                            # Data keywords (BROAD)  
                            data_keywords = [
                                'data', 'analytics', 'analyst',
                                'intelligence', 'insights', 'science',
                                'quantitative', 'reporting', 'bi '
                            ]
                            
                            # Design keywords (BROAD)
                            design_keywords = [
                                'ux', 'ui', 'design', 'designer',
                                'user experience', 'user interface',
                                'visual', 'graphic', 'interaction',
                                'research', 'prototype'
                            ]
                            
                            has_pm = any(kw in title_lower for kw in pm_keywords)
                            has_data = any(kw in title_lower for kw in data_keywords)
                            has_design = any(kw in title_lower for kw in design_keywords)
                            
                            # Accept if matches ANY category
                            if not (has_pm or has_data or has_design):
                                continue
                            
                            # ONLY exclude pure software engineering
                            pure_swe_excludes = [
                                'software engineer intern',
                                'software development intern',
                                'backend engineer intern',
                                'frontend engineer intern',
                                'full stack engineer intern',
                                'devops engineer intern'
                            ]
                            
                            if any(exclude in title_lower for exclude in pure_swe_excludes):
                                continue
                            
                            # ACCEPT IT!
                            job_id = url.split('/')[-1].split('?')[0] if url else str(int(time.time()))
                            
                            category = ""
                            if has_pm:
                                category = "📦 PM/Product"
                            elif has_data:
                                category = "📈 Data/Analytics"
                            elif has_design:
                                category = "🎨 Design"
                            
                            job = {
                                'job_id': f"linkedin_{job_id}",
                                'title': title,
                                'company': company,
                                'location': location_text,
                                'url': url,
                                'source': 'LinkedIn (24hrs)'
                            }
                            
                            jobs.append(job)
                            print(f"      ✓ {category} {title[:50]}...")
                    
                    except Exception as e:
                        continue
                
                print(f"    ✅ Kept {len(jobs)} jobs")
            else:
                print(f"    ⚠️  Status: {response.status_code}")
        
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        return jobs