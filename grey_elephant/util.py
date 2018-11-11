import smtplib
from flask import url_for

def sendemail(send_email, access_code):
    subject = 'Merry Gift Giving!'
    message = 'Click the link to receive a gift from your friend! Link: https://central-diagram-222007.appspot.com/' + url_for("refer") + \
              "\n Access Code:" + access_code
    smtpserver = 'smtp.gmail.com:587'
    password = 'HackerFooBar123'
    login = 'greyelephantstaff@gmail.com'
    to_addr_list = [send_email]
    from_addr = 'greyelephantstaff@gmail.com'
    print("function got called")

    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

    return problems