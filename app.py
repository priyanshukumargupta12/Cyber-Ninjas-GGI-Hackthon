from flask import Flask, request, render_template, send_file, abort
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'app/uploads'
OUTPUT_FOLDER = 'output'  # Updated to match main.py
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        apk_file = request.files['apk']
        if apk_file:
            filename = secure_filename(apk_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            apk_file.save(filepath)

            # Run your analysis tool (e.g., main.py)
            subprocess.run(['python3', 'main.py', filepath, OUTPUT_FOLDER])

            # Check if the JSON report exists
            report_path = os.path.join(OUTPUT_FOLDER, "report.json")
            print(f"Looking for report at: {report_path}")  # Debugging log
            if not os.path.exists(report_path):
                print(f"Error: Report file not found at {report_path}")
                abort(404, description="Report file not found")

            # Send the JSON report as a downloadable file
            return send_file(report_path, as_attachment=True)
    return render_template('index.html')
