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

@app.route("/recipientinfo/", methods=["GET"])
def recipient_info():
    form = RecipientForm(request.form)
    return render_template("recipient_info_form.html", form=form, error=False)

@app.route("/recipientinfo/", methods=["POST"])
def recipient_info_post():
    form = RecipientForm(request.form)
    if form.validate():
        pass
        # data = scrape(form.instagram.data)
    else:
        return render_template("recipient_info_form.html", form=form, error=True)
    return str(form.data)

@app.route("/results")
def results():
    return render_template("results.html")


if __name__ == "__main__":
    app.run()