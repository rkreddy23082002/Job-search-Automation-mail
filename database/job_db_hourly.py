import sqlite3
from datetime import datetime

class JobDatabaseHourly:
    def __init__(self, db_path="jobs_hourly.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE,
                title TEXT,
                company TEXT,
                location TEXT,
                url TEXT,
                description TEXT,
                posted_date TEXT,
                scraped_date TEXT,
                source TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def job_exists(self, job_id):
        """Check if job already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE job_id = ?', (job_id,))
        exists = cursor.fetchone()[0] > 0
        
        conn.close()
        return exists
    
    def add_job(self, job_data):
        """Add new job"""
        try:
            if self.job_exists(job_data['job_id']):
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO jobs (job_id, title, company, location, url, description, posted_date, scraped_date, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data['job_id'],
                job_data['title'],
                job_data['company'],
                job_data['location'],
                job_data['url'],
                job_data.get('description', ''),
                job_data.get('posted_date', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                job_data['source']
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"      ❌ DB error: {e}")
            return False
    
    def get_recent_jobs(self):
        """Get jobs from last 24 hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        from datetime import timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        cursor.execute('SELECT * FROM jobs WHERE scraped_date >= ?', (yesterday,))
        jobs = cursor.fetchall()
        
        conn.close()
        return jobs