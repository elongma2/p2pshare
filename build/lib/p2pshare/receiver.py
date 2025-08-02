# recieve on phone
import qrcode
from flask import Flask, send_file
import io
from .utils import get_local_ip_udp,shutdown_server
from waitress import serve
app = Flask(__name__)
FILE_PATH = None  # Global placeholder

def generate_qrcode_to_receive(ip):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"http://{ip}:5000/download")
    qr.make(fit=True)

    f = io.StringIO()
    qr.print_ascii(out=f)
    print(f"\nScan this QR to download your file:\n{f.getvalue()}")

@app.route("/download")
def download():
    return send_file(FILE_PATH, as_attachment=True)

def run_receiver(filepath,timeout = None):
    global FILE_PATH
    FILE_PATH = filepath
    ip = get_local_ip_udp()
    generate_qrcode_to_receive(ip)
    print(f"Or open manually: http://{ip}:5000/download")
    if timeout:
        shutdown_server(timeout)
    serve(app, host='0.0.0.0', port=5000)
    
