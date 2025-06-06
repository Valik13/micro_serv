from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/message", methods=["GET"])
def get_message():
    return jsonify({"message": "Це статичне повідомлення з messages-service"})


if __name__ == "__main__":
    app.run(port=5002)