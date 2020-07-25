from flask import Flask, jsonify, request, session, flash, render_template
from register import upload_user_data, upload_slot_data, upload_entrance_test_data
from db import students, db
from datetime import timedelta

app = Flask(__name__)
app.debug = True


app.config["SECRET_KEY"] = "fmq049kbjmajf734nvadinhfg"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)


@app.route("/welcome", methods=["GET"])
def welcome():
    return jsonify({"data": "Success"})


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/register/userdata", methods=["GET","POST"])
def register_user_data():
    if request.method == "POST":
        print(request.form)
        # name = request.form["name"]
        # email = request.form["email"]
        # password = request.form["password"]
        # dob = request.form["dob"]
        # aadhar_no = request.form["aadhar_no"]
        # address = request.form["address"]
        # entrance_score = request.form["entrance_score"]
        # is_enrolled = request.form["is_enrolled"]
        # slot_preference_1 = request.form["slot_preference_1"]
        # slot_preference_2 = request.form["slot_preference_2"]
        # slot_preference_3 = request.form["slot_preference_3"]
        # slot_preference_4 = request.form["slot_preference_4"]
        # batch_id = request.form["batch_id"]
        # upload_user_data(name, email, password, dob, aadhar_no, address, entrance_score, is_enrolled, slot_preference_1, slot_preference_2, slot_preference_3, slot_preference_4, batch_id)
        session.permanent = True
        session["email"] = "email"
        return render_template("baseline_quiz.html")
    else:
        return render_template("register.html")


@app.route("/register/entrance_test_data", methods=["GET", "POST"])
def register_entrance_test_data():
    if request.method == "POST":
        print(request.form)
        return render_template("slots.html")
    else:
        return render_template("baseline_quiz.html")

@app.route("/register/slots_preference", methods=["GET","POST"])
def register_slot_data():
    if request.method == "POST":
        print(request.form)
        return "Application Submitted"
    else:
        return render_template("slots.html")

db.init_app(app)
db.create_all(app=app)

if __name__ == '__main__':
    app.run()
