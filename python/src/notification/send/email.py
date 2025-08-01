import smtplib, os, json, logging
import json
from email.message import EmailMessage



def notification(message) -> str | None:
    try:
        message = json.loads(message)
        email_content = EmailMessage()
        email_content.set_content(f"Your MP3 file is ready: {message['mp3_fid']}")
        email_content["Subject"] = "MP3 File Ready"
        email_content["From"] = os.environ.get("SMTP_USER")
        email_content["To"] = message['user_name']

        logging.info(f"Sending email to {message['user_name']} with content: {email_content}")

        # Implement the actual email sending logic here
        session = smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"))
        session.starttls()
        session.login(os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASS"))
        session.send_message(email_content, email_content["From"], email_content["To"])
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return str(e)
