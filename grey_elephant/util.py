import smtplib


def sendemail():
    subject = 'Merry Gift Giving!'
    message = 'Click the link to receive a gift from your friend! Link: http://127.0.0.1:5000/login'
    smtpserver = 'smtp.gmail.com:587'
    password = 'HackerFooBar123'
    login = 'greyelephantstaff@gmail.com'
    to_addr_list = [form.email.data]
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