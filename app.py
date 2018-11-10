from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from grey_elephant import RecipientForm

app = Flask(__name__)
app.template_folder = "./templates"
Bootstrap(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/recipientinfo/", methods=["GET"])
def recipient_info():
    form = RecipientForm(request.form)
    return render_template("recipient_info_form.html", form=form, error=False)

@app.route("/recipientinfo/", methods=["POST"])
def recipient_info_post():
    form = RecipientForm(request.form)
    if form.validate():
        print(form.data)
    else:
        return render_template("recipient_info_form.html", form=form, error=True)
    return str(form.data)

@app.route("/results")
def results():
    return render_template("results.html")

app.run()