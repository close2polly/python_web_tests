from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from email.mime.text import MIMEText
import smtplib
import yaml

with open("email_info.yaml") as f:
    email_info = yaml.safe_load(f)


def send_email():
    fromaddr = email_info["login"]
    toaddr = email_info["login"]
    mypass = email_info["password"]
    reportname = "log.log"
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Отчет о тестировании"
    with open(reportname, "rb") as f:
        part = MIMEApplication(f.read(), Name=basename(reportname))
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(reportname)
        msg.attach(part)
    body = "Тесты завершены"
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


send_email()