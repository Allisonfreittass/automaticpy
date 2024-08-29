import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

download_folder = os.path.expanduser("~/Downloads")
pdf_folder = os.path.expanduser("~/Documents/PDFs")
image_folder = os.path.expanduser("~/Pictures")
application_folder = os.path.expanduser("~/Applications")

os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)
os.makedirs(application_folder, exist_ok=True)

file_types = {
    ".pdf": pdf_folder,
    ".jpg": image_folder,
    ".jpeg": image_folder,
    ".png": image_folder,
    ".gif": image_folder,
    ".exe": application_folder,
    ".msi": application_folder,
}

class DownloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(download_folder):
            source = os.path.join(download_folder, filename)
            if os.path.isfile(source):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in file_types:
                    destination_folder = file_types[file_ext]
                    shutil.move(source, destination_folder)
                    print(f"Movido {filename} para {destination_folder}")

if __name__ == "__main__":
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, download_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
