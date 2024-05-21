from data.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Sender:
    def __init__(self):
        self.email = settings.EMAIL
        self.pswrd = settings.EMAILPSWRD
        self.server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        self.server.login(self.email, self.pswrd)
        self.server.auth_plain()

    def send_mail(self, mailto, mail_theme, mail_text):

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = mailto
        msg['Subject'] = mail_theme

        msg.attach(
                MIMEText(mail_text, 'plain', 'utf-8')
            )
        self.server.send_message(msg)
