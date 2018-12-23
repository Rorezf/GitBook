# Email

## Send

### Smtp

```text
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendMail(content, athFile, subject):
    user = "xx@yy.com"
    sender = "NAME<" + user + ">"
    receiver = ['xx2@yy.com', 'xx3@yy.com']

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ";".join(receiver)
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    with open(athFile, 'rb') as f:
        attach = MIMEBase('xls', 'xls', filename=athFile)
        attach.add_header('Content-Disposition', 'attachment', filename=athFile)
        attach.add_header('Content-ID', '<0>')
        attach.add_header('X-Attachment-Id', '0')
        attach.set_payload(f.read())
        encoders.encode_base64(attach)
        msg.attach(attach)

    server = smtplib.SMTP()
    server.connect("zz.com")
    server.login(user, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
```

## Receive

### IMAP

```text
from imapclient import IMAPClient
self.server = IMAPClient(HOST, use_uid=True, ssl=False)
self.server.login(base64.b64decode(USERNAME), PASSWORD)
self.server.logout()

def getSpecialEmailContent(self):
    self.server.select_folder('INBOX')
    messages = self.server.search(['SINCE', datetime.date.today()])
    response = self.server.fetch(messages, ['RFC822'])

    for msgid, data in response.iteritems():
        msg_string = data['RFC822']
        msg = email.message_from_string(msg_string)
        if not "Field Issues for week" in msg['Subject']:
            continue
        subjectName = msg['Subject'].split(" for ")[1]

        if msg.get_content_maintype() == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    mailContent = part.get_payload(decode=True)

    if not 'mailContent' in dir():
        mailContent, subjectName = "", ""
    self.tearDown()
    return mailContent, subjectName
```

