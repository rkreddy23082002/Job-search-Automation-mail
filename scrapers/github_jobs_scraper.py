import requests
import re
import time

class GitHubJobsScraper:
    def __init__(self):
        self.repos = [
            "SimplifyJobs/Summer2025-Internships",
            "pittCSC/Summer2025-Internships"
        ]
        self.base_url = "https://raw.githubusercontent.com"
    
    def search_jobs(self, keyword_filter=None):
        """Scrape internship repos on GitHub"""
        jobs = []
        
        for repo in self.repos:
            try:
                print(f"    Fetching from GitHub: {repo}...")
                
                # Get README content
                url = f"{self.base_url}/{repo}/main/README.md"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 404:
                    url = f"{self.base_url}/{repo}/master/README.md"
                    response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Find all markdown links with pattern [Text](URL)
                    # These repos typically format as: [Company Name](application-link) | Role | Location | etc
                    
                    job_count = 0
                    lines = content.split('\n')
                    
                    for line in lines:
                        # Skip if not a table row or doesn't have links
                        if not ('|' in line and '[' in line and '](' in line):
                            continue
                        
                        # Skip header/separator rows
                        if '---' in line or 'Company' in line or 'Location' in line:
                            continue
                        
                        try:
                            # Extract company name and URL from markdown link
                            company_match = re.search(r'\[([^\]]+)\]\(([^\)]+)\)', line)
                            if not company_match:
                                continue
                            
                            company = company_match.group(1)
                            url_found = company_match.group(2)
                            
                            # Clean emojis and special chars
                            company = re.sub(r'[🔒↗️✅❌🛂📝]', '', company).strip()
                            
                            # Split the line by pipes to get other info
                            parts = [p.strip() for p in line.split('|')]
                            
                            # Try to find role and location in the parts
                            role = ''
                            location = 'Various'
                            
                            for part in parts:
                                part_clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', part).strip()
                                part_clean = re.sub(r'[🔒↗️✅❌🛂📝]', '', part_clean).strip()
                                
                                if not part_clean or part_clean == company:
                                    continue
                                
                                # Role usually contains "Intern" or "Engineering"
                                if 'intern' in part_clean.lower() and not role:
                                    role = part_clean
                                # Location usually has state codes or "Remote"
                                elif any(loc in part_clean for loc in ['Remote', 'Hybrid', 'US', 'CA', 'NY', 'TX']) and location == 'Various':
                                    location = part_clean
                            
                            # If no role found, try to construct one
                            if not role:
                                role = f"Software Engineering Intern"
                            
                            # Only add if we have minimum info and it's an intern role
                            if company and 'intern' in role.lower():
                                # Apply keyword filter if provided
                                if keyword_filter and keyword_filter.lower() not in role.lower():
                                    continue
                                
                                job = {
                                    'job_id': f"github_{repo.split('/')[1]}_{company.replace(' ', '_')}_{int(time.time())}",
                                    'title': role,
                                    'company': company,
                                    'location': location,
                                    'url': url_found if url_found.startswith('http') else f'https://github.com/{repo}',
                                    'source': 'GitHub'
                                }
                                
                                jobs.append(job)
                                job_count += 1
                                
                                # Show first few
                                if job_count <= 5:
                                    print(f"      ✓ {role[:40]} at {company}")
                        
                        except Exception as e:
                            continue
                    
                    if job_count > 5:
                        print(f"      ... and {job_count - 5} more")
                    elif job_count == 0:
                        print(f"      ⚠️ Repo format might have changed - found 0 jobs")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        return jobs