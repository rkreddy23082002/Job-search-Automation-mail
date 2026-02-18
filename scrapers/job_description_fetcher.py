import requests
from bs4 import BeautifulSoup

class JobDescriptionFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def fetch_linkedin_description(self, url):
        """Fetch full job description from LinkedIn"""
        try:
            print(f"  📄 Fetching description from: {url[:50]}...")
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple selectors for job description
                desc_elem = (
                    soup.find('div', class_='show-more-less-html__markup') or
                    soup.find('div', class_='description__text') or
                    soup.find('section', class_='description') or
                    soup.find('div', {'class': 'decorated-job-posting__details'})
                )
                
                if desc_elem:
                    text = desc_elem.get_text(separator='\n', strip=True)
                    print(f"  ✅ Fetched {len(text)} characters")
                    return text[:8000]  # Limit to 8000 chars
                
                print("  ⚠️  Description element not found")
                return "Description not available - please copy from LinkedIn manually"
            
            print(f"  ❌ HTTP {response.status_code}")
            return f"Could not fetch (Status: {response.status_code})"
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return f"Error fetching description: {str(e)}"