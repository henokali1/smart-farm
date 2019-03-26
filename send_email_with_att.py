import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ntpath

def email_sender(email = 't.project3333@gmail.com',
                 password = 'projectpsw',
                 send_to_email = 't.project3333@gmail.com',
                 subject = 'This is the subject',
                 message = 'This is my message',
                 file_location = 'unhealthy_leaf.png'):

    msg = MIMEMultipart()

    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    body = message

    msg.attach(MIMEText(body, 'plain'))

    filename = ntpath.basename(file_location)
    attachment = open(file_location, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    try:
        server.sendmail(email, send_to_email, text)
        print("email sent")
    except:
        print("Sending email failed")
    server.quit()
