from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.template_folder = "./template"
Bootstrap(app)

@app.route("/")
def root():
    return "Hello World!"

@app.route("/hack")
def hack():
    return render_template("index.html")
app.run()