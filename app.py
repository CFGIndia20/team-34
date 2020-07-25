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

if __name__ == '__main__':
    app.run()
