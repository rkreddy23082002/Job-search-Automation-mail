from flask import Flask, render_template, request, jsonify
from database.job_db import JobDatabase
from datetime import datetime
import os

app = Flask(__name__)

def get_category(title):
    """Determine job category from title"""
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
    """Get category display label"""
    category = get_category(title)
    labels = {
        'pm': '📦 PM/Product',
        'data': '📈 Data/Analytics',
        'design': '🎨 Design'
    }
    return labels.get(category, '📦 PM/Product')

app.jinja_env.globals.update(get_category=get_category)
app.jinja_env.globals.update(get_category_label=get_category_label)

@app.route('/')
def index():
    """Homepage - Show all jobs"""
    try:
        db = JobDatabase()
        jobs = db.get_todays_jobs()
        
        return render_template('index.html', 
                             jobs=jobs, 
                             total=len(jobs))
    except Exception as e:
        return f"""
        <div style='padding: 40px; text-align: center; font-family: Arial;'>
            <h1>⚠️ Dashboard Error</h1>
            <p style='color: #666; margin: 20px 0;'>{str(e)}</p>
            <p>Make sure you've run <code>python main.py</code> first to populate the database!</p>
            <br>
            <a href='/' style='padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;'>
                Retry
            </a>
        </div>
        """

@app.route('/api/jobs')
def get_jobs_api():
    """API endpoint - Get jobs as JSON"""
    try:
        db = JobDatabase()
        jobs = db.get_todays_jobs()
        
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
                'category': get_category(job[2])
            })
        
        return jsonify({
            'jobs': jobs_list,
            'total': len(jobs_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/copy-job', methods=['POST'])
def copy_job_details():
    """Format job for Claude chat"""
    data = request.json
    
    formatted = f"""Hey Claude! Help me tailor my resume for this job:

Job Title: {data.get('title')}
Company: {data.get('company')}
Location: {data.get('location')}
Job URL: {data.get('url')}

Please:
1. Tailor my resume to emphasize relevant experience
2. Generate a compelling cover letter
3. Suggest which projects to highlight

I'll paste my resume and job description below.
"""
    
    return jsonify({'formatted_text': formatted, 'success': True})

@app.route('/mark-applied', methods=['POST'])
def mark_applied():
    """Mark job as applied"""
    data = request.json
    job_id = data.get('job_id')
    
    return jsonify({
        'success': True, 
        'message': f'Marked job {job_id} as applied!',
        'job_id': job_id
    })

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    """Trigger main.py scraper from dashboard"""
    import subprocess
    import threading
    
    def run_in_background():
        try:
            result = subprocess.run(
                ['python', 'main.py'], 
                capture_output=True, 
                text=True,
                timeout=180
            )
            print("✅ Scraper completed")
        except Exception as e:
            print(f"❌ Scraper error: {e}")
    
    thread = threading.Thread(target=run_in_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Job scraper started! New jobs will appear in ~2 minutes.'
    })

@app.route('/stats')
def get_stats():
    """Get application statistics"""
    try:
        db = JobDatabase()
        jobs = db.get_todays_jobs()
        
        stats = {
            'total': len(jobs),
            'pm': len([j for j in jobs if get_category(j[2]) == 'pm']),
            'data': len([j for j in jobs if get_category(j[2]) == 'data']),
            'design': len([j for j in jobs if get_category(j[2]) == 'design'])
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Job Application Dashboard Starting...")
    print("="*60)
    print("\n📍 Open your browser to: http://localhost:5001")
    print("🎯 Features:")
    print("   ✅ Filter by category (PM/Data/Design)")
    print("   ✅ Search jobs")
    print("   ✅ Sort by date/company/title")
    print("   ✅ Dark mode")
    print("   ✅ Track applied jobs")
    print("   ✅ Copy for Claude (free AI tailoring)")
    print("   ✅ Auto-refresh every 5 minutes")
    print("   ✅ Run scraper from dashboard")
    print("\n💡 Make sure 'jobs.db' exists (run main.py first)")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, port=5001, host='0.0.0.0')