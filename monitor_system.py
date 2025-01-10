import psutil
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

import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'bayo01@yuslord.com'
EMAIL_PASSWORD = 'Yuslord07%'  # Use an app-specific password or environment variable.

# Slack configuration
SLACK_TOKEN = 'hku4a3KsmlEExbHebvu2MHKc'
SLACK_CHANNEL = '#alertntn'

# Send email notification
def send_email(subject, message):
    try:
        msg = MIMEText(message)
        msg['First Script Test'] = subject
        msg['Bayo01@yuslord.com'] = EMAIL_ADDRESS
        msg['Bayo01@yuslord.com'] = EMAIL_ADDRESS  # Change to recipient's email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Send Slack notification
def send_slack_notification(message):
    client = WebClient(token=SLACK_TOKEN)
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        logging.info(f"Slack alert sent: {response['ts']}")
    except SlackApiError as e:
        logging.error(f"Slack API error: {e.response['error']}")

# Modify alert functions to include notifications
def handle_high_cpu():
    logging.info("Attempting to resolve high CPU usage...")
    highest_proc = max(psutil.process_iter(['pid', 'cpu_percent']), key=lambda p: p.info['cpu_percent'])
    highest_proc.terminate()
    message = f"High CPU usage resolved by terminating process {highest_proc.info['pid']}."
    logging.info(message)
    send_email("High CPU Usage Alert", message)
    send_slack_notification(message)

def handle_low_disk_space():
    logging.info("Attempting to clear disk space...")
    temp_dir = '/tmp'
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except Exception as e:
                logging.error(f"Failed to delete {file}: {e}")
    message = "Low disk space detected. Temporary files cleared."
    logging.info(message)
    send_email("Low Disk Space Alert", message)
    send_slack_notification(message)
