from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from grey_elephant import RecipientForm
from ig_scrape import scrape

app = Flask(__name__)
app.template_folder = "./templates"
Bootstrap(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():

    return render_template("home.html")

@app.route("/recipientinfo/", methods=["GET"])
def recipient_info():
    form = RecipientForm(request.form)
    return render_template("recipient_info_form.html", form=form, error=False)

@app.route("/recipientinfo/", methods=["POST"])
def recipient_info_post():
    form = RecipientForm(request.form)

    import smtplib

    def sendemail(from_addr = 'greyelephantstaff@gmail.com', to_addr_list = [form.email.data],
                  subject = 'Merry Gift Giving!', message = 'Click the link to receive a gift from your friend! Link: http://127.0.0.1:5000/login',
                  login = 'greyelephantstaff@gmail.com', password = 'HackerFooBar123',
                  smtpserver='smtp.gmail.com:587'):
        print "function got called"

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

    if form.validate():
        sendemail()
        # data = scrape(form.instagram.data)
    else:
        return render_template("recipient_info_form.html", form=form, error=True)
    return str(form.data)

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/aboutgreyelephant/")
def aboutgreyelephant():
    return render_template("aboutgreyelephant.html")

if __name__ == "__main__":
    app.run()