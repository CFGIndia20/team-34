from flask import Flask, jsonify, request, session, redirect, render_template
import repo
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "geeksforsocialchange"
app.debug = True

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


#################################################################
##                     Registration 1st page
#################################################################


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



#################################################################
##                     Registration 2nd Page
#################################################################


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


#################################################################
##                     Registration 3rd page
#################################################################


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


#################################################################
##                     Teacher shoot up link
#################################################################


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


#################################################################
##                     Teacher add - shoot up link
#################################################################


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




#################################################################
##                     Placement Candidate
#################################################################

@app.route("/placement/candidate", methods=["GET", "POST"])
def placement_candidate():
    if request.method == "GET":
        ob = repo.OhlcRepo()
        company = ob.find_records_with_sort_field(collection_name="companies", query={}, field='salary')
        return render_template("placement_candidate.html", companies=company)




#################################################################
##                     Placement Employer
#################################################################


@app.route("/placement/employer", methods=["GET", "POST"])
def placement_employer():
    if request.method == "GET":
        ob = repo.OhlcRepo()
        candidates = ob.find_records_with_sort_field(collection_name="students", query={}, field='marks')
        return render_template("placement_employer.html", candidates=candidates)



#################################################################
##                     Student Schedule
#################################################################

@app.route("/students/schedule", methods=["GET", "POST"])
def student_schedule():
    session["email"] = "someone@gmail.com"
    ob = repo.OhlcRepo()
    student = ob.find_records_with_query(collection_name="students", query={"email":session["email"]})[0]
    batchid = student.batch_id
    ob1 = repo.OhlcRepo()
    teachers = ob1.find_records(collection_name="teachers")
    for teacher in teachers:
        for batch in teacher.batch_list:
            if batchid == batch:
                link = batch.link
                slot = batch.slot
                teacher_name = teacher.name

    data = jsonify({
        "link": link,
        "batch": student.batch_id,
        "slot": slot,
        "teacher": teacher_name,
    })
    return render_template("student_schedule.html", data=data)




#################################################################
##                     Student Analytics
#################################################################

@app.route("/students/analytics", methods=["GET", "POST"])
def student_analytics():
    session["email"] = "someone@gmail.com"
    ob = repo.OhlcRepo()
    student = ob.find_records_with_query(collection_name="students", query={"email":session["email"]})[0]
    data = jsonify({
        "marks": student.marks,
        "attendance": student.attendance
    })
    return render_template("student_marks&attendance.html", data=data)




#################################################################
##                     Teacher Schedule
#################################################################


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


#################################################################
##                     Admin View Batches
#################################################################


@app.route("/admin/view_batches", methods=["GET", "POST"])
def view_batch_list():
    if request.method == 'GET':
        return render_template("view_batches.html")
    else:
        session["email"] = "someone@gmail.com"
        ob = repo.OhlcRepo()
        batches = []
        teachers = ob.find_records_with_query(collection_name="teachers", query={"email":session["email"]})
        for teacher in teachers:
            batch_list = teacher.batch_list
            for batch in batch_list:
                batches.append(batch)
        return batches

#################################################################
##                     Admin View Teachers
#################################################################  

@app.route("/admin/view_teachers", methods=["GET", "POST"])
def view_teachers_list():
    if request.method == 'GET':
        return render_template("view_teachers.html")
    else:
        session["email"] = "someone@gmail.com"
        ob = repo.OhlcRepo()
        data = []
        teachers = ob.find_records_with_query(collection_name="teachers", query={"email":session["email"]})
        for teacher in teachers:
            data.append({
                "name": teacher.name,
                "batches": teacher.batch_list
            })
        return data

#################################################################
##                   Student - Batch Mapping
#################################################################  

listofstudents = []
slot_frequency = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
students_allotted = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
batches = []

def giveMeRandom4Slots():
    ans = []
    while(len(ans) != 4):
        my_random_slot = random.randint(1,13)
        if(my_random_slot not in ans):
            ans.append("slot" + str(my_random_slot))
    return ans

def rankMyChoices(choices):
    ans = []
    for i in range(0,4):
        ans.append(slot_frequency[choices[i]]%15)
    return choices.index(min(choices))

@app.route("/admin/students_allocation", methods=["GET", "POST"])
def admin_students_allocation():

    ob = repo.OhlcRepo()
    results = ob.find_record_with_projection(collection_name="students", query={}, projection={"email": 1, "p1": 1, "p2": 1, "p3": 1, "p4": 1})
    
    listofstudents = []
    for entry in results:
        listofstudents.append([entry["email"], [int(entry["p1"][4:]), int(entry["p2"][4:]), int(entry["p3"][4:]), int(entry["p4"][4:])]])

    for i in listofstudents:
        chosen_slot = rankMyChoices(i[1])
        slot_frequency[i[1][chosen_slot]] += 1
        students_allotted[i[1][chosen_slot]].append(i[0])

    #for i in students_allotted:
    #    print(i)

    batch_number = 1
    one_batch = []
    for i in range(len(students_allotted)):
        for j in students_allotted[i]:
            if(len(one_batch) < 15):
                one_batch.append(j)
            else:
                batches.append([batch_number, i, one_batch])
                batch_number += 1
                one_batch = []
                one_batch.append(j)
        if(len(one_batch) > 0):
            batches.append([batch_number, i, one_batch])
            batch_number += 1
            one_batch = []

    batch_dict = {}
    for i in batches:
        batch = i[0]
        slot = i[1]
        for email in i[2]:
            batch_dict[str(batch)] = slot
            ob.update_query(collection_name="students", query_doc={"email": email}, insert_doc={"batch_id": batch, "slot": slot})
        print(i)

    for batch in batch_dict:
        ob.insert_record_one(collection_name="batches", insert_doc={"batch": batch, "slot": batch_dict[batch]})

def checkIfSomeTecherIsEmpty(teachers):
    for i in teachers:
        if(len(i[2]) == 0):
            return 1
    return 0

#################################################################
##                Teachers - Batch Allocation
#################################################################  

@app.route("/admin/teachers_allocation", methods=["GET", "POST"])
def admin_teachers_allocation():

    ite = 0

    ob = repo.OhlcRepo()
    results1 = ob.find_record_with_projection(collection_name="batches", query={}, projection={"batch": 1, "slot": 1})
    results2 = ob.find_record_with_projection(collection_name="teachers", query={}, projection={"email": 1})

    data = []
    for entry in results1:
        data.append([(entry["batch"]), int(entry["slot"]), 0])

    teachers = []
    for entry in results2:
        teachers.append([entry["email"], 0, []])

    print(teachers)
    print(data)
    while (checkIfSomeTecherIsEmpty(teachers)):
        for i in range(len(data)):
            while (data[i][2] == 0):
                current_selection = random.randint(0,len(teachers)-1)
                if(teachers[current_selection][1] < 4):
                    do_we_reject = 0
                    maximum_difference = 0
                    for j in teachers[current_selection][2]:
                        maximum_difference = max(maximum_difference,abs(data[i][1]-j[1]))
                        if(abs(j[1]-data[i][1]) <= 1):
                            do_we_reject = 1
                            break
                    if(do_we_reject == 1):
                        continue
                    elif(maximum_difference > 8):
                        continue
                    else:
                        teachers[current_selection][2].append([data[i][0],data[i][1]])
                        teachers[current_selection][1] += 1
                        data[i][2] = 1
        ite+=1
        print(ite)

    for i in teachers:
        print(i)

        assigned = []
        for entry in i[2]:
            assigned.append({"batch" : entry[0], "slot": entry[1]})

        ob.update_query(collection_name="teachers", query_doc={"email": i[0]}, insert_doc={"assigned": assigned})
        

if __name__ == '__main__':
    app.run()
