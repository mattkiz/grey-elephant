from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
from grey_elephant import RecipientForm, util
from grey_elephant.models import User, Session, Recipient
import uuid
import facebook
from machine_learning.use_machine_learning import use_machine_learning



app = Flask(__name__)
app.template_folder = "./templates"
Bootstrap(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    session = Session()
    response_body = request.json.get("authResponse")
    if session.query(User.fb_id).filter(User.fb_id==int(response_body.get("userID"))).count() == 0:
        graph = facebook.GraphAPI(response_body.get("accessToken"), version="2.12")
        user_fb = graph.get_object(int(response_body.get("userID")))
        firstname = user_fb.get("name").split(" ")[0]
        lastname = user_fb.get("name").split(" ")[1]
        new_user = User(uuid=str(uuid.uuid4()), firstname=firstname, lastname=lastname,
                        fb_access_token=response_body.get("accessToken"),
                        fb_id=int(user_fb.get("id")))
        session.add(new_user)
        session.commit()
        r = make_response(render_template("home.html"))
        r.set_cookie("uuid", new_user.uuid)
        return r

@app.route("/refer", methods=["GET"])
def refer_get():
    return render_template("refer.html")

@app.route("/refer", methods=["POST"])
def refer():
    session = Session()
    response_body = request.json.get("authResponse")
    if session.query(User.fb_id).filter(User.fb_id==int(response_body.get("userID"))).count() == 0:
        ref_code = request.json.get("refCode")
        print(ref_code)
        ref_user = session.query(User).get(ref_code)
        graph = facebook.GraphAPI(response_body.get("accessToken"), version="2.12")
        user_fb = graph.get_object(int(response_body.get("userID")))
        firstname = user_fb.get("name").split(" ")[0]
        lastname = user_fb.get("name").split(" ")[1]
        new_user = User(uuid=str(uuid.uuid4()), firstname=firstname, lastname=lastname,
                        fb_access_token=response_body.get("accessToken"),
                        fb_id=int(user_fb.get("id")))
        new_recp = Recipient(uuid=str(uuid.uuid4()))
        ref_user.recipient.append(new_recp)
        session.add(new_user)
        session.add(new_recp)
        token = str(new_user.fb_access_token)
        #Redirect to display page, call it there when budget is set
        #data = use_machine_learning(token, budget=55)
        session.commit()
    return render_template("home.html")

@app.route("/recipientinfo/", methods=["GET"])
def recipient_info():
    form = RecipientForm(request.form)
    return render_template("recipient_info_form.html", form=form, error=False)

@app.route("/recipientinfo/", methods=["POST"])
def recipient_info_post():
    form = RecipientForm(request.form)
    if form.validate():
        uuid_cookie = request.cookies.get("uuid")
        util.sendemail(form.email.data, uuid_cookie)
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