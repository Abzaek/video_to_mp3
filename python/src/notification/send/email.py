import smtplib, os, json
import json


def notification(message) -> str | None:
    try:
        message = json.loads(message)
        email_content = f"Your MP3 file is ready: {message['mp3_fid']}"
        
        # Here you would implement the actual email sending logic
        # For example, using smtplib or any other email service
        print(f"Sending email to {message['email']} with content: {email_content}")

        # Implement the actual email sending logic here
        with smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT")) as server:
            server.starttls()
            server.login(os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASS"))
            server.sendmail(os.environ.get("SMTP_USER"), message['user_name'], email_content)

    except Exception as e:
        print(f"Error sending email: {e}")
        return str(e)