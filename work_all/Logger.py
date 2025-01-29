import os
import datetime

class Logger:
    def __init__(self, directory, start=True, pr=False):
        self.active = start
        self.directory = directory
        self.print = pr
        
        if not self.active:
            return None
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"log_{timestamp}.txt"
        
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        self.log_path = os.path.join(directory, self.log_file)
        
        # Create empty log file
        with open(self.log_path, "w") as f:
            pass
            
    def log_to_file(self, message):
        if not self.active:
            return
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_path, "a", encoding='utf-8') as f:
            f.write(log_entry)
        
        if self.print:     
            print(log_entry)

