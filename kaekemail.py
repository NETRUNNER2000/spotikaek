import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up the server and email details
smtp_server = 'smtp.gmail.com'  # Gmail's SMTP server
smtp_port = 587  # For TLS
sender_email = 'netrunner.devs@gmail.com'
receiver_email = 'shaahid.adams@gmail.com'
password = 'yiov myxj orrz nfpm'  # Use an app-specific password if using Gmail 2FA


def send_success_email(total_added_tracks, message_data):
    sucess_subject = 'Automation successfully executed - {0} Tracks Synchronised'.format(total_added_tracks)
    sucess_body = message_data
    send_email(sucess_subject, sucess_body)

def send_failed_email():
    failed_subject = 'Automation failed to execute correctly'
    failed_body = "You suck at coding, noob"
    send_email(failed_subject, failed_body)


def send_email(subject, body):
    # Set up MIME (Multipurpose Internet Mail Extensions) for the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg['X-Priority'] = '1'
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the server, login, and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, password)  # Login to your email account
            text = msg.as_string()  # Convert the MIME message to a string
            server.sendmail(sender_email, receiver_email, text)  # Send the email
    except Exception as e:
        print(f'Error: {e}')
