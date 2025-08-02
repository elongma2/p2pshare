import argparse
import os
import shutil
from .sender import run_sender
from .receiver import run_receiver

def main():
    parser = argparse.ArgumentParser(description="p2pshare CLI tool")
    parser.add_argument('--send', action='store_true', help="Phone sends file to PC (upload)")
    parser.add_argument('--receive', action='store_true', help="PC sends file to phone (download)")
    parser.add_argument('path', nargs='?', help="Path to file or folder (used with --receive)")
    parser.add_argument('--timeout',type=int, help="Auto-shutdown server based on your desired time (in seconds)")
    args = parser.parse_args()

    if args.receive:
        file_path = args.path
        if not file_path:
            print("❌ Error: Missing file path after --receive")
            print("Usage: python main.py --receive path/to/file")
            exit(1)
        if not os.path.exists(args.path):
            print("❌ File or folder does not exist.")
            exit(1)
        if os.path.isdir(file_path):
            print("📦 Zipping folder before sending...")
            zip_path = shutil.make_archive(file_path, 'zip', file_path)
            file_path = zip_path  # override to point to the zip file
        run_receiver(filepath = file_path, timeout = args.timeout)
    elif args.send:
        run_sender(timeout = args.timeout)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
