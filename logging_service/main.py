from flask import Flask, request, jsonify

app = Flask(__name__)
logs = []
unique_messages = set()

@app.route("/log", methods=["POST"])
def log_message():
    data = request.get_json()
    message = data.get("message")
    if message:
        if message not in unique_messages:
            logs.append(message)
            unique_messages.add(message)
        return jsonify({"status": "logged"}), 200
    return jsonify({"error": "No message provided"}), 400

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs), 200

if __name__ == "__main__":
    app.run(port=5001)