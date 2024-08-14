import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from jinja2 import Template

SMTP_SERVER_HOST = 'localhost'
# SMTP_SERVER_HOST = 'smtp.gmail.com'
SMTP_SERVER_PORT = 1025
# SMTP_SERVER_PORT = 587
SENDER_ADDRESS = 'support@E-Library.com'
SENDER_PASSWORD = ''

def send_email(to_address, subject, message, content='text', attachment_file=None):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    
    if content == 'html':
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))
    
    if attachment_file:
        try:
            with open(attachment_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition', f'attachment; filename={os.path.basename(attachment_file)}',
                )
                msg.attach(part)
        except Exception as e:
            print(f"Failed to attach file: {e}")
    
    try:
        with smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT) as s:
            # s.starttls()  # Uncomment if using TLS
            s.login(SENDER_ADDRESS, SENDER_PASSWORD)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def format_message(template_file, data={}):
    try:
        with open(template_file) as file:
            template = Template(file.read())
            return template.render(data=data)
    except Exception as e:
        print(f"Failed to format message: {e}")
        return ""