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
        ob = repo.OhlcRepo()
        company = ob.find_records_with_sort_field(collection_name="companies", query={}, field='salary')
        return render_template("placement_candidate.html", companies=company)


@app.route("/placement/employer", methods=["GET", "POST"])
def placement_employer():
    if request.method == "GET":
        ob = repo.OhlcRepo()
        candidates = ob.find_records_with_sort_field(collection_name="students", query={}, field='marks')
        return render_template("placement_employer.html", candidates=candidates)


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

@app.route("/teachers/schedule", methods=["GET", "POST"])
def teachers_schedule():
    if request.method == "GET":
        session["email"] = "teacher@gmail.com"

        ob = repo.OhlcRepo()
        results = ob.find_record_with_projection(collection_name="teachers", query={"email": session["email"]}, projection={"assigned": 1})[0]
        assigned = results["assigned"]
        
        schedule = []
        slot_mapping = {1: "7am - 8am", 2: "8am - 9am", 3: "9am - 10am", 4: "10am - 11am", 5: "11am - 12pm", 6: "12pm - 1pm",
        7: "1pm - 2pm", 8: "2pm - 3pm", 9: "3pm - 4pm", 10: "4pm - 5pm", 11: "5pm - 6pm", 12: "6pm - 7pm", 13: "7pm - 8pm"}

        for entry in assigned:
            timing = slot_mapping[entry["slot"]]
            if entry["batch_id"]:
                schedule.append({"slot": timing, "batch": entry["batch_id"]})
            else:
                schedule.append({"slot": timing, "batch": "--"})

        print(schedule)
        return render_template("teacher_schedule.html", schedule=schedule)

#################################################################
##                     Teacher Attendance
#################################################################


@app.route("/teacher_batches_attendance", methods=["GET", "POST"])
def teacher_batches_attendance():
    if request.method == 'GET':
        # Assuming session data is available
        session["email"] = "teacher@gmail.com"

        ob = repo.OhlcRepo()
        results = ob.find_record_with_projection(collection_name="teachers", query={"email": session["email"]}, projection={"assigned": 1})[0]

        assigned = results["assigned"]
        batch_ids = []
        for entry in assigned:
            batch_ids.append(entry["batch_id"])

        return render_template('teacher_attendance.html', batch_ids=batch_ids)

    elif request.method == 'POST':

        print("Request Form: ", request.form)
        print("Len: ", len(request.form))
        if len(request.form) ==  1:
            batch_id = request.form["batch"]
            print("Batch ID: ", batch_id)
            ob = repo.OhlcRepo()

            results = ob.find_record_with_projection(collection_name="teachers", query={"email": session["email"]}, projection={"assigned": 1})[0]
            assigned = results["assigned"]
            batch_ids = []
            for entry in assigned:
                batch_ids.append(entry["batch_id"])

            print("Batch type: ", type(batch_id))
            results = ob.find_record_with_projection(collection_name="students", query={"batch_id": float(batch_id)}, projection={"email": 1, "name": 1, "attendance": 1})
            print("Students: ", results)
            return render_template('teacher_attendance.html', batch_ids=batch_ids, students=results)
        
        else:

            ob = repo.OhlcRepo()
            print(request.form)
            for email in request.form:
                print(email)
                attendance = request.form[email]
                ob.update_query(collection_name="students", query_doc={"email": email}, insert_doc={"attendance": attendance})

            return render_template('teacher_dashboard.html')


#################################################################
##                     Teacher Marks
#################################################################


@app.route("/teacher_batches_marks", methods=["GET", "POST"])
def teacher_batches_marks():
    if request.method == 'GET':
        # Assuming session data is available
        session["email"] = "teacher@gmail.com"

        ob = repo.OhlcRepo()
        results = ob.find_record_with_projection(collection_name="teachers", query={"email": session["email"]}, projection={"assigned": 1})[0]

        assigned = results["assigned"]
        batch_ids = []
        for entry in assigned:
            batch_ids.append(entry["batch_id"])

        return render_template('teacher_assignmarks.html', batch_ids=batch_ids)

    elif request.method == 'POST':

        print("Request Form: ", request.form)
        print("Len: ", len(request.form))
        if len(request.form) ==  1:
            batch_id = request.form["batch"]
            print("Batch ID: ", batch_id)
            ob = repo.OhlcRepo()

            results = ob.find_record_with_projection(collection_name="teachers", query={"email": session["email"]}, projection={"assigned": 1})[0]
            assigned = results["assigned"]
            batch_ids = []
            for entry in assigned:
                batch_ids.append(entry["batch_id"])

            print("Batch type: ", type(batch_id))
            results = ob.find_record_with_projection(collection_name="students", query={"batch_id": float(batch_id)}, projection={"email": 1, "name": 1, "marks": 1})
            print("Students: ", results)
            return render_template('teacher_assignmarks.html', batch_ids=batch_ids, students=results)
        
        else:

            ob = repo.OhlcRepo()
            print(request.form)
            for email in request.form:
                print(email)
                marks = request.form[email]
                ob.update_query(collection_name="students", query_doc={"email": email}, insert_doc={"marks": marks})

            return render_template('teacher_dashboard.html')
    

if __name__ == '__main__':
    app.run()
