import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, receiver):
    message = MIMEMultipart()
    message['From'] = "aarbiasim@gmail.com"
    message['To'] = ", ".join(receiver)
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("aarbiasim@gmail.com", "bgcgzttawflbowqt")
            server.sendmail("aarbiasim@gmail.com", receiver, message.as_string())
            print('Email sent successfully.')
    except smtplib.SMTPException as e:
        print(f'Failed to send email. Error: {str(e)}')
