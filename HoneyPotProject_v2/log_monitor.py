import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from models import LogEntry, db_session

class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("cowrie.json"):
            with open(event.src_path, 'r') as f:
                for line in f:
                    log_entry = LogEntry(log_type='cowrie', message=line.strip())
                    db_session.add(log_entry)
                    db_session.commit()

def start_monitoring():
    path = 'cowrie/logs'
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    observer.join()
