import random 
import smtplib
from email.message import EmailMessage

otp=""

for i in range(6):
    otp += str(random.randint(0,9))

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
from_mail = "judesamuelsjj@gmail.com" 
server.login(from_mail,"vueq onyq ufxw kjod")
to_mail = input("Enter your email address: ")
msg = EmailMessage()
msg['Subject'] = "OTP-Verification"
msg['From'] = from_mail
msg['To'] = to_mail
msg.set_content("Hello This is your OTP-Verification code to login is " + otp)

try:
    server.send_message(msg)
    print("Email sent successfully")
except TypeError:
    raise {"Incorrect email or password"}

