from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.template_folder = "./templates"
Bootstrap(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/recipientinfo", methods=["GET"])
def recipient_info():
    return "Rec_Info"

@app.route("/recipientinfo", methods=["POST"])
def recipient_info_post():
    return "Rec_Info_Post"

@app.route("/results")
def results():
    return render_template("results.html")

app.run()