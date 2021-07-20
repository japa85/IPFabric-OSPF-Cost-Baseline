# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


def send(sender, target, server, subject, email_body):

    msg = MIMEText(email_body)

    msg['Subject'] = subject
    msg['From'] = sender

    s = smtplib.SMTP(server)
    s.sendmail(sender, target, msg.as_string())
