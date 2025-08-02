import socket
import os
import time
import threading
import logging

logging.basicConfig(filename='server.log', 
                        level= logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_local_ip_udp():
    # Create a UDP socket
    # AF_INET specifies IPv4, SOCK_DGRAM specifies UDP
    sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) #Internet,Udp
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

def shutdown_server(s):  
    def shut_down():
        print(f"⏳ Auto-shutdown timer started ({s} seconds)...")
        time.sleep(s)
        print("💥 Time's up. Server shutting down.")
        os._exit(0)
    threading.Thread(target=shut_down, daemon=True).start()

def log_file(file_path,start_time):
    try:
        #get size of file
        size_byte = os.path.getsize(file_path)
        size = size_byte / 1024
        filename = os.path.basename(file_path)
        duration = time.time() - start_time
        logging.info(f"Uploaded: {filename} | Size: {size:.2f} KB | Duration: {duration:.2f} seconds")
    except Exception as e:
        logging.error(f"Error logging file: {e}")


