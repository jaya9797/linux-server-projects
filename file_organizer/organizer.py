import os
import shutil
from pathlib import Path
from datetime import datetime

# Setup directories
HOME_DIR = Path.home()
PROJECT_DIR = HOME_DIR / "projects" / "file_organizer"
DOWNLOADS_DIR = PROJECT_DIR / "downloads"
LOGS_ARCHIVE = DOWNLOADS_DIR / "Logs"
HEALTH_REPORT = HOME_DIR / "health_report.txt"
WEB_FILE = Path("/var/www/html/index.html")

def integrate_all_projects():
    print("--- Starting Master Integration Loop ---")
    
    # 1. Ensure directories exist
    LOGS_ARCHIVE.mkdir(parents=True, exist_ok=True)
    
    # 2. Check if a new health report exists from Project 1
    report_content = "No recent health report data found."
    if HEALTH_REPORT.exists():
        # Read the stats
        with open(HEALTH_REPORT, "r") as f:
            report_content = f.read()
        
        # Project 2 Automation: Move and timestamp the old report into the Logs Archive folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = LOGS_ARCHIVE / f"health_report_{timestamp}.txt"
        shutil.move(str(HEALTH_REPORT), str(archive_name))
        print(f"[Project 2] Archived system health data to: {archive_name.name}")
    else:
        print("[Project 2] No raw health report file found in home directory. Using cached view.")

    # 3. Project 3 Automation: Generate a live HTML Dashboard for Nginx
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Master Operations Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #1e1e24; color: #f5f5f5; text-align: center; padding-top: 50px; }}
        .container {{ width: 80%; max-width: 700px; margin: auto; background: #2a2a35; padding: 30px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); border-top: 5px solid #00adb5; }}
        h1 {{ color: #00adb5; margin-bottom: 5px; }}
        .status {{ display: inline-block; padding: 5px 10px; background: #23a950; color: white; border-radius: 4px; font-size: 0.9em; font-weight: bold; margin-bottom: 20px; }}
        pre {{ text-align: left; background: #111116; padding: 20px; border-radius: 8px; font-family: 'Courier New', monospace; overflow-x: auto; color: #393e46; border-left: 3px solid #ff2e63; color: #a6e22e; }}
        .footer {{ margin-top: 20px; font-size: 0.8em; color: #777; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Server Control Dashboard 📊</h1>
        <div class="status">ALL SYSTEMS OPERATIONAL</div>
        <p>Live resource metrics compiled by Python automation script:</p>
        <pre>{report_content}</pre>
        <div class="footer">Last dashboard rebuild: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
</body>
</html>"""

    # Write the file directly to Nginx web directory using system permissions if allowed
    try:
        with open(PROJECT_DIR / "index.html", "w") as f:
            f.write(html_template)
        # Safely copy to the protected Nginx folder using sudo
        os.system(f"sudo cp {PROJECT_DIR}/index.html {WEB_FILE}")
        print("[Project 3] Nginx web dashboard compiled and successfully updated!")
    except Exception as e:
        print(f"Error compiling web page: {e}")

if __name__ == "__main__":
    integrate_all_projects()
