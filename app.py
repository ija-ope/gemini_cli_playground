import os
import subprocess
import json
from flask import Flask, render_template, redirect, url_for, send_from_directory
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Define the path to the screenshot archive directory
ARCHIVE_DIR = os.path.expanduser("~/Documents/old files")
SCRIPT_PATH = os.path.expanduser("~/screenshot_archives/organize_screenshots.sh")

def get_archive_stats():
    """Calculates statistics about the archive directory."""
    if not os.path.exists(ARCHIVE_DIR):
        # Return empty/default stats if the directory doesn't exist
        return 0, 0, [], json.dumps([]), json.dumps([]), 0

    files = [f for f in os.listdir(ARCHIVE_DIR) if f.lower().endswith('.png')]
    file_count = len(files)
    total_size = sum(os.path.getsize(os.path.join(ARCHIVE_DIR, f)) for f in files)
    
    # Process data for the chart
    activity_by_day = defaultdict(int)
    for f in files:
        mod_time = os.path.getmtime(os.path.join(ARCHIVE_DIR, f))
        day = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
        activity_by_day[day] += 1
        
    sorted_days = sorted(activity_by_day.keys())
    chart_labels = json.dumps(sorted_days)
    chart_data = json.dumps([activity_by_day[day] for day in sorted_days])
    
    num_days = len(activity_by_day)
    average_per_day = round(file_count / num_days if num_days > 0 else 0, 2)
    
    return file_count, total_size, files, chart_labels, chart_data, average_per_day

def format_size(size_bytes):
    """Formats a size in bytes into a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/1024**2:.2f} MB"
    else:
        return f"{size_bytes/1024**3:.2f} GB"

@app.route('/')
def dashboard():
    """The main dashboard route."""
    file_count, total_size, files, chart_labels, chart_data, average_per_day = get_archive_stats()
    readable_size = format_size(total_size)
    
    # Sort files by modification time, newest first
    # This check is important because 'files' might be empty
    if files:
        files.sort(key=lambda f: os.path.getmtime(os.path.join(ARCHIVE_DIR, f)), reverse=True)

    return render_template('dashboard.html', 
                           file_count=file_count, 
                           total_size=readable_size,
                           files=files,
                           chart_labels=chart_labels,
                           chart_data=chart_data,
                           average_per_day=average_per_day)

@app.route('/run-script')
def run_script():
    """Executes the screenshot organization script."""
    # This will not work on Render, but we leave it for local execution.
    # A more robust implementation would disable this button if the script doesn't exist.
    if os.path.exists(SCRIPT_PATH):
        try:
            subprocess.run(['/bin/bash', SCRIPT_PATH], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e.stderr}")
            return redirect(url_for('dashboard', error=e.stderr))
    return redirect(url_for('dashboard'))

@app.route('/view/<path:filename>')
def view_file(filename):
    """Serves a specific file from the archive for viewing."""
    # This will likely result in a 404 on Render if the ARCHIVE_DIR doesn't exist, which is acceptable.
    return send_from_directory(ARCHIVE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
