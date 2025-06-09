from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logs = []
unique_messages = set()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.route("/log", methods=["POST"])
def log_message():
    data = request.get_json()
    message = data.get("message") if data else None
    if not message:
        return jsonify({"error": "No message provided"}), 400
    if message not in unique_messages:
        logs.append(message)
        unique_messages.add(message)
        logger.info(f"New message logged: {message}")
    else:
        logger.info(f"Duplicate message skipped: {message}")
    return jsonify({"status": "logged"}), 200

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs), 200

@app.route("/", methods=["GET"])
def index():
    return "Logging Service is running!"

if __name__ == "__main__":
    app.run(port=5001)