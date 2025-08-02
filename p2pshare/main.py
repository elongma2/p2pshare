import argparse
import os
import shutil
from .sender import run_sender
from .receiver import run_receiver
import zipfile 

def main():
    parser = argparse.ArgumentParser(description="p2pshare CLI tool")
    parser.add_argument('--send', action='store_true', help="Phone sends file to PC (upload)")
    parser.add_argument('--receive', action='store_true', help="PC sends file to phone (download)")
    parser.add_argument('paths',nargs='*', help="Paths to files or folders (used with --send)")
    parser.add_argument('--timeout',type=int, help="Auto-shutdown server based on your desired time (in seconds)")
    args = parser.parse_args()

    if args.receive:
        if args.paths:
            if len(args.paths) == 1:
                path = args.paths[0]
                if not os.path.exists(path):
                    print("❌ File or folder does not exist.")
                    exit(1)
                if os.path.isdir(path):
                    print("📦 Zipping folder before sending...")
                    zip_path = shutil.make_archive(path, 'zip', path)
                    path = zip_path  # override to point to the zip file
            else: #mutiple files
                valid_files = []
                for path in args.paths:
                    if os.path.exists(path):
                        valid_files.append(path)
                    else:
                        print(f"❌ Skipping Non-existent file or folder: {path}")
                if not valid_files:
                    print("❌ No valid files found.")
                    exit(1)
                print("📦 Zipping multiple files...")
                zip_path = "p2pshare_bundle.zip"
                with zipfile.ZipFile(zip_path,'w') as zipf:
                    for file in valid_files:
                        if os.path.isdir(file):
                            for root,_,files in os.walk(file):
                                for f in files:
                                    full_path = os.path.join(root,f)
                                    arcname = os.path.relpath(full_path,os.path.dirname(file)) #allow relative paths to start from dirname
                                    zipf.write(full_path,arcname)
                        else:
                            arcname = os.path.basename(file)
                            zipf.write(file,arcname)
                path = zip_path  # override to point to the zip file
            run_receiver(filepath = path, timeout = args.timeout)
    elif args.send:
        run_sender(timeout = args.timeout)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
