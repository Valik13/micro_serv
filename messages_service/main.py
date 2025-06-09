from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route("/message", methods=["GET"])
def get_message():
    response = make_response(jsonify({"message": "Це статичне повідомлення з messages-service"}))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route("/", methods=["GET"])
def index():
    return "Messages Service is running!"

if __name__ == "__main__":
    app.run(port=5002)