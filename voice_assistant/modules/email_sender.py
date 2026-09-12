"""
email_sender.py
Sends an email via voice command using smtplib.

IMPORTANT (see README privacy section): use a dedicated TEST/DUMMY email
account for this, never your personal account, since credentials are read
from environment variables and the assistant sends whatever body text it
is given.

For Gmail: enable 2FA on the dummy account, then create an "App Password"
(Google Account -> Security -> App Passwords) and use that instead of the
real account password.
"""

import os
import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.environ.get("ASSISTANT_EMAIL_ADDRESS")
        self.sender_password = os.environ.get("ASSISTANT_EMAIL_APP_PASSWORD")

    def send_email(self, recipient: str, subject: str, body: str) -> str:
        if not self.sender_email or not self.sender_password:
            return (
                "I can't send email because no test email account is "
                "configured (ASSISTANT_EMAIL_ADDRESS / "
                "ASSISTANT_EMAIL_APP_PASSWORD)."
            )

        if not recipient or "@" not in recipient:
            return "I don't have a valid recipient address to send that to."

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = recipient

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, [recipient], msg.as_string())
            return f"Email sent to {recipient}."
        except smtplib.SMTPException as e:
            return f"I couldn't send the email: {e}"
