import requests
from bs4 import BeautifulSoup
import time

class LinkedInHourlyScraper:
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    def search_jobs(self, keyword, location="United States", max_results=50):
        """Search LinkedIn - LAST 1 HOUR - Filter for PM/Data/Design"""
        jobs = []
        
        try:
            print(f"    Searching (1hr): {keyword}...")
            
            # Last 1 hour = 3600 seconds
            params = f"?keywords={keyword.replace(' ', '%20')}&location={location}&f_JT=I&f_TPR=r3600"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            url = self.base_url + params
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')
                
                if len(job_cards) > 0:
                    print(f"    Found {len(job_cards)} jobs, filtering...")
                
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
                            
                            # Skip aggregators
                            if company in ['Lensa', 'Jobs via Dice']:
                                continue
                            
                            # === CHECK YOUR 3 CATEGORIES ===
                            
                            # PM/Product keywords (BROAD)
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
                            
                            # Must match at least ONE category
                            if not (has_pm or has_data or has_design):
                                continue
                            
                            # Only exclude pure software engineering
                            pure_swe = [
                                'software engineer intern',
                                'backend engineer intern',
                                'frontend engineer intern',
                                'devops engineer intern'
                            ]
                            
                            if any(swe in title_lower for swe in pure_swe):
                                continue
                            
                            # ACCEPT IT!
                            job_id = url.split('/')[-1].split('?')[0] if url else str(int(time.time()))
                            
                            category = "📦 PM" if has_pm else ("📈 DATA" if has_data else "🎨 DESIGN")
                            
                            job = {
                                'job_id': f"linkedin_hourly_{job_id}",
                                'title': title,
                                'company': company,
                                'location': location_text,
                                'url': url,
                                'source': 'LinkedIn (1hr)'
                            }
                            
                            jobs.append(job)
                            print(f"      🔥 {category} {title[:45]}...")
                    
                    except Exception as e:
                        continue
                
                if len(jobs) > 0:
                    print(f"    ✅ Kept {len(jobs)} relevant jobs")
        
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        return jobs