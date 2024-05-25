from data.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Sender:
    def __init__(self):
        self.server = None
        self.email = settings.EMAIL
        self.pswrd = settings.EMAILPSWRD



    def send_mail(self, mailto, mail_theme, mail_text):
        self.server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        self.server.login(self.email, self.pswrd)
        self.server.auth_plain()
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = mailto
        msg['Subject'] = mail_theme

        msg.attach(
                MIMEText(mail_text, 'plain', 'utf-8')
            )
        self.server.send_message(msg)
        self.server.quit()
