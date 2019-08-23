from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class Notifier:
    def __init__(self, password, targetEmail, subject, body):
        self._NOTIFIER_EMAIL = "frankgastle@gmail.com"
        self._password = password
        self._targetEmail = targetEmail
        self._body = body
        self._subject = subject
        self._message = self.buildMessage()

    def _buildMessage(self):
        msg = MIMEMultipart()
        msg['From'] = self.NOTIFIER_EMAIL
        msg['To'] = self.targetEmail
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body, 'plain'))
        return msg
    
    def send(self):
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.login(self.NOTIFIER_EMAIL, self.password)
        text = self.message.as_string()
        server.sendmail(self.NOTIFIER_EMAIL, self.targetEmail, text)
        server.quit()











        
