from flask import Flask, render_template, request, jsonify
from database.job_db import JobDatabase
from datetime import datetime, timedelta
import os
import subprocess
import threading

app = Flask(__name__)

def get_category(title):
    """Determine job category"""
    title_lower = title.lower()
    
    pm_keywords = ['product', 'program', 'project', 'management', 'manager', 'strategy', 'operations']
    data_keywords = ['data', 'analytics', 'analyst', 'intelligence', 'insights', 'science', 'quantitative', 'bi ']
    design_keywords = ['ux', 'ui', 'design', 'designer', 'visual', 'graphic', 'interaction']
    
    if any(kw in title_lower for kw in pm_keywords):
        return 'pm'
    elif any(kw in title_lower for kw in data_keywords):
        return 'data'
    elif any(kw in title_lower for kw in design_keywords):
        return 'design'
    else:
        return 'pm'

def get_category_label(title):
    """Get category label"""
    category = get_category(title)
    labels = {
        'pm': '📦 PM/Product',
        'data': '📈 Data/Analytics',
        'design': '🎨 Design'
    }
    return labels.get(category, '📦 PM/Product')

def is_last_hour(scraped_date):
    """Check if job was scraped in last hour"""
    try:
        job_time = datetime.strptime(scraped_date, '%Y-%m-%d %H:%M:%S')
        one_hour_ago = datetime.now() - timedelta(hours=1)
        return job_time >= one_hour_ago
    except:
        return False

app.jinja_env.globals.update(get_category=get_category)
app.jinja_env.globals.update(get_category_label=get_category_label)
app.jinja_env.globals.update(is_last_hour=is_last_hour)

@app.route('/')
def index():
    """Homepage"""
    try:
        db = JobDatabase()
        
        # Clean up old unapplied jobs first
        deleted = db.cleanup_old_unapplied_jobs()
        if deleted > 0:
            print(f"🗑️  Cleaned up {deleted} old unapplied jobs")
        
        # Get all jobs from last 24 hours
        all_jobs = db.get_todays_jobs()
        last_hour = db.get_last_hour_jobs()
        applied = db.get_applied_jobs()
        
        return render_template('index.html', 
                             jobs=all_jobs,
                             total=len(all_jobs),
                             last_hour_count=len(last_hour),
                             applied_count=len(applied))
    except Exception as e:
        return f"""
        <div style='padding: 40px; text-align: center; font-family: Arial;'>
            <h1>⚠️ Dashboard Error</h1>
            <p style='color: #666; margin: 20px 0;'>{str(e)}</p>
            <p>Run <code>python main.py</code> first!</p>
            <br>
            <a href='/' style='padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;'>
                Retry
            </a>
        </div>
        """

@app.route('/api/jobs')
def get_jobs_api():
    """Get jobs as JSON"""
    try:
        db = JobDatabase()
        jobs = db.get_todays_jobs()
        last_hour_jobs = db.get_last_hour_jobs()
        
        last_hour_ids = {job[1] for job in last_hour_jobs}
        
        jobs_list = []
        for job in jobs:
            jobs_list.append({
                'id': job[0],
                'job_id': job[1],
                'title': job[2],
                'company': job[3],
                'location': job[4],
                'url': job[5],
                'scraped_date': job[8],
                'source': job[9],
                'applied': job[10] if len(job) > 10 else 0,
                'category': get_category(job[2]),
                'is_last_hour': job[1] in last_hour_ids
            })
        
        return jsonify({
            'jobs': jobs_list,
            'total': len(jobs_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mark-applied', methods=['POST'])
def mark_applied():
    """Mark job as applied in database"""
    data = request.json
    job_id = data.get('job_id')
    
    try:
        db = JobDatabase()
        db.mark_as_applied(job_id)
        
        return jsonify({
            'success': True,
            'message': 'Marked as applied!',
            'job_id': job_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    """Trigger scraper"""
    def run_in_background():
        try:
            subprocess.run(['python', 'main.py'], capture_output=True, timeout=180)
            print("✅ Scraper completed")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    thread = threading.Thread(target=run_in_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Scraper started! Refresh in 2 minutes.'
    })
@app.route('/get-description', methods=['POST'])
def get_description():
    """Fetch job description from URL"""
    from scrapers.job_description_fetcher import JobDescriptionFetcher
    
    data = request.json
    url = data.get('url')
    
    try:
        fetcher = JobDescriptionFetcher()
        description = fetcher.fetch_linkedin_description(url)
        
        return jsonify({
            'success': True,
            'description': description
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Job Application Dashboard")
    print("="*60)
    print("\n📍 Open: http://localhost:5001")
    print("\n✨ Features:")
    print("   🔥 Last hour jobs highlighted")
    print("   📊 24-hour job feed")
    print("   ✅ Applied job tracking")
    print("   🗑️  Auto-cleanup old unapplied jobs")
    print("   🔄 Auto-refresh every 5 min")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, port=5001, host='0.0.0.0')