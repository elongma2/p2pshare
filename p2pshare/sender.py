#send from phone
import os
import qrcode
import io
from flask import Flask,request,render_template_string
from werkzeug.utils import secure_filename
from .utils import get_local_ip_udp,shutdown_server,log_file
from waitress import serve
import time

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip','docx','esv'}
UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

# Inline HTML template for upload page
HTML_STRING = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Upload File to PC</title>
<style>
    body {
    font-family: sans-serif;
    background-color: #f5f5f5;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    }
    .upload-container {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    text-align: center;
    width: 300px;
    }
    input[type="file"] {
    margin: 1rem 0;
    }
    button {
    padding: 0.6rem 1.2rem;
    border: none;
    background-color: #007bff;
    color: white;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    }
    button:hover {
    background-color: #0056b3;
    }
    h2 {
    margin-bottom: 1rem;
    }
</style>
</head>
<body>
<div class="upload-container">
    <h2>Upload to PC</h2>
    <form method="POST" enctype="multipart/form-data" action="/upload">
    <input type="file" name="files" multiple required>
    <br>
    <button type="submit">Upload</button>
    </form>
</div>
</body>
</html>
"""

def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

def generate_qrcode_to_upload(ip):
    qr = qrcode.QRCode(
        version= 1,
        error_correction= qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"http://{ip}:5001/upload")
    qr.make(fit=True)
    f = io.StringIO()
    qr.print_ascii(out=f)
    print(f"\nScan this QR to upload a file:\n{f.getvalue()}")


@app.route('/upload', methods= ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        #check if the post request has the file part
        if 'files' not in request.files:
            return 'No file part in request'
        
        files = request.files.getlist('files')
        sucess = 0
        for file in files:
            if file.filename == '':
                return 'No file selected'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                start_time= time.time()
                file.save(save_path)
                log_file(save_path,start_time)
                sucess += 1

        return f"✅ {sucess} file(s) uploaded successfully"
    return render_template_string(HTML_STRING)

# Entry point
def run_sender(timeout = None):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    ip = get_local_ip_udp()
    generate_qrcode_to_upload(ip)
    print(f"Or open manually: http://{ip}:5001/upload")
    if timeout:
        shutdown_server(timeout)
    serve(app, host='0.0.0.0', port=5001)
    

