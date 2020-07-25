from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.debug = True


@app.route("/welcome", methods=["GET"])
def welcome():
    return jsonify({"data": "Success"})

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
