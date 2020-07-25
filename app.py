from flask import Flask, jsonify, request, session, redirect, render_template
import repo
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "geeksforsocialchange"
app.debug = True

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/register/userdata", methods=["GET", "POST"])
def register_userdata():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        print("Into register userdata")
        form = {}
        print(request.form)

        form["name"] = request.form["name"]
        form["email"] = request.form["email"]
        form["password"] = request.form["pwd"]
        form["dob"] = request.form["dob"]
        form["aadhar_no"] = request.form["aadhar"]
        form["address"] = request.form["address"]

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(form["password"].encode(), salt)
        form["password"] = hashed

        ob = repo.OhlcRepo()
        print(ob)
        ob.insert_record_one(collection_name="students",insert_doc=form)

        session.permanent = True
        session["email"] = form["email"]

        return redirect("/register/entrance_test")

@app.route("/register/entrance_test", methods=["GET", "POST"])
def register_entrance():
    if request.method == 'GET':
        return render_template('baseline_quiz.html')
    elif request.method == 'POST':
        form = {}
        if request.args:
            form["score"] = request.args.get("score")
            form["email"] = session["email"]
            
            ob = repo.OhlcRepo()
            results = ob.find_record_with_projection(collection_name="students", query={"email": form["email"]}, projection={"email": 1})
            if len(results) != 1:
                return jsonify({"error": "Student not found"})
            ob.update_one(collection_name="students",query={"email": form["email"]},insert_doc={"$set":form})

        return redirect("/register/slots_preference")

@app.route("/register/slots_preference", methods=["GET", "POST"])
def register_slots():
    if request.method == 'GET':
        return render_template('slots.html')
    elif request.method == 'POST':
        form = {}
        print(request.form)
        print("\n\n")
        
        form["p1"] = request.form["p1"]
        form["p2"] = request.form["p2"]
        form["p3"] = request.form["p3"]
        form["p4"] = request.form["p4"]
        form["email"] = session["email"]
        
        ob = repo.OhlcRepo()
        results = ob.find_record_with_projection(collection_name="students", query={"email": form["email"]}, projection={"email": 1})
        if len(results) != 1:
            return jsonify({"error": "Student not found"})
        ob.update_one(collection_name="students",query={"email": form["email"]},insert_doc={"$set":form})

        return jsonify({"data": "Success"})


@app.route("/teacher/shoot_link", methods=["GET", "POST"])
def shoot_link():
    session["email"] = "someone@gmail.com"
    if request.method == "GET":
        return render_template("teacher_shoot_link.html", data = "TESTING")
    else:
        email = session["email"]
        ob = repo.OhlcRepo()
        teacher = ob.find_records_with_querys(collection_name="teachers", query={"email": email})[0]
        batches = teacher.batches
        return batches


@app.route("/teacher/update_shoot_link", methods=["GET", "POST"])
def update_shoot_link():
    session["email"] = "someone@gmail.com"
    if request.method == "GET":
        return render_template("teacher_shoot_link.html", data="TESTING")
    else:
        form = {}
        print(request.form)
        batch_id = request.form["batch_id"]
        date = request.form["date"]
        time = request.form["time"]
        link = request.form["link"]

        email = session["email"]
        ob = repo.OhlcRepo()
        teacher = ob.find_records_with_querys(
            collection_name="teachers", query={"email": email})[0]
        batches = teacher.batches
        for obj in batches:
            if obj.batch_id == batch_id :
                obj.video.append({
                    "date": date,
                    "time": time,
                    "link": link
                })
        ob.update_query(collection_name="teachers", query_doc={"email": email}, insert_doc={"batches":batches})[0]
        return jsonify({"data": "Success"})

@app.route("/placement/candidate", methods=["GET", "POST"])
def placement_candidate():
    if request.method == "GET":
        return render_template("placement_candidate.html", data="TESTING")
    else:
        session["email"] = "someone@gmail.com"
        ob = repo.OhlcRepo()
        company = ob.find_records("companies")
        return company


@app.route("/placement/employer", methods=["GET", "POST"])
def placement_employer():
    if request.method == "GET":
        return render_template("placement_employer.html", data="TESTING")
    else:
        session["email"] = "someone@gmail.com"
        ob = repo.OhlcRepo()
        students = ob.find_records("students")
        return students


@app.route("/students/analytics", methods=["GET", "POST"])
def candidate_placement():
    if request.method == "GET":
        return render_template("student_analytics.html", data="TESTING")
    else:
        session["email"] = "someone@gmail.com"
        ob = repo.OhlcRepo()
        student = ob.find_records_with_query(collection_name="students", query={"email":session["email"]})[0]
        data = jsonify({
            "marks": student.marks,
            "attendance": student.attendance
        })
        return data


    


    


if __name__ == '__main__':
    app.run()
