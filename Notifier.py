from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class Notifier:
    def __init__(self, password, notifierEmail, targetEmail, subject, body):
        self.NOTIFIER_EMAIL = notifierEmail
        self.password = password
        self.targetEmail = targetEmail
        self.body = body
        self.subject = subject
        self.message = self.buildMessage()

    def buildMessage(self):
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











        
