import sqlite3
from datetime import datetime, timedelta

class JobDatabase:
    def __init__(self, db_path="jobs.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create tables with applied tracking"""
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
                source TEXT,
                applied BOOLEAN DEFAULT 0,
                applied_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def job_exists(self, job_id):
        """Check if job exists"""
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
                INSERT INTO jobs (job_id, title, company, location, url, description, posted_date, scraped_date, source, applied)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
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
    
    def get_todays_jobs(self):
        """Get all jobs from last 24 hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        twenty_four_hours_ago = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT * FROM jobs 
            WHERE scraped_date >= ?
            ORDER BY scraped_date DESC
        ''', (twenty_four_hours_ago,))
        
        jobs = cursor.fetchall()
        conn.close()
        return jobs
    
    def get_last_hour_jobs(self):
        """Get jobs from last 1 hour"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT * FROM jobs 
            WHERE scraped_date >= ?
            ORDER BY scraped_date DESC
        ''', (one_hour_ago,))
        
        jobs = cursor.fetchall()
        conn.close()
        return jobs
    
    def mark_as_applied(self, job_id):
        """Mark a job as applied"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE jobs 
            SET applied = 1, applied_date = ?
            WHERE job_id = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_applied_jobs(self):
        """Get all jobs marked as applied"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs 
            WHERE applied = 1
            ORDER BY applied_date DESC
        ''')
        
        jobs = cursor.fetchall()
        conn.close()
        return jobs
    
    def cleanup_old_unapplied_jobs(self):
        """Delete unapplied jobs older than 24 hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        twenty_four_hours_ago = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            DELETE FROM jobs 
            WHERE scraped_date < ? AND applied = 0
        ''', (twenty_four_hours_ago,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted