from gpiozero import LightSensor
from picamera import PiCamera
from time import sleep
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders


camera = PiCamera()
ldr = LightSensor(4)

ldr.when_dark = lambda: caught()

def caught():
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/image.jpg')
    sleep(2)
    camera.stop_preview()

    me = 'cocosimms2020@gmail.com'
    send_to_email = 'tul13214@temple.edu'
    subject = 'INTRUDER! SECURITY ALERT!'
    message = 'Someone triggered the system. We sent you a picture.'
    message = MIMEText(message)

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = send_to_email
    msg.preamble = "test"
    msg.attach(message)

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open('image.jpg', 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename = "image.jpg"')
    msg.attach(part)

    try:
        print('Sending Email')
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user = 'cocosimms2020@gmail.com', password = 'yamski2002')
        s.sendmail(me, send_to_email, msg.as_string())
        s.quit()
        print('Email Sent!')
    except SMTPException as error:
        print('Error: Unable to send email alert.')


        
                    

