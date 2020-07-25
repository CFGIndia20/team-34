from flask import Flask, jsonify

app = Flask(__name__)
app.debug = True


@app.route("/welcome", methods=["GET"])
def welcome():
    return jsonify({"data": "Success"})


if __name__ == '__main__':
    app.run()
