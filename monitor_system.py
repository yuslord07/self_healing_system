import psutil # type: ignore
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='system_health.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    logging.info(f"CPU Usage: {cpu_usage}%")
    logging.info(f"Memory Usage: {memory.percent}%")
    logging.info(f"Disk Usage: {disk.percent}%")
    
    # Check thresholds
    if cpu_usage > 80:
        logging.warning("High CPU Usage Detected!")
        handle_high_cpu()
    if memory.percent > 80:
        logging.warning("High Memory Usage Detected!")
    if disk.percent > 90:
        logging.warning("Low Disk Space Detected!")
        handle_low_disk_space()

def handle_high_cpu():
    logging.info("Attempting to resolve high CPU usage...")
    # Example: Kill the most resource-heavy process
    highest_proc = max(psutil.process_iter(['pid', 'cpu_percent']), key=lambda p: p.info['cpu_percent'])
    highest_proc.terminate()
    logging.info(f"Terminated process {highest_proc.info['pid']} to resolve CPU usage.")

def handle_low_disk_space():
    logging.info("Attempting to clear disk space...")
    # Example: Clear temp files (adjust path as needed)
    import os
    temp_dir = '/tmp'  # Change this for Windows (e.g., C:\\Windows\\Temp)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except Exception as e:
                logging.error(f"Failed to delete {file}: {e}")

if __name__ == "__main__":
    log_system_metrics()
