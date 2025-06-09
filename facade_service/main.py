from flask import Flask, request, jsonify, make_response
import requests
import time
import logging

app = Flask(__name__)
MESSAGES_SERVICE_URL = "http://localhost:5002/message"
LOGGING_SERVICE_URL = "http://localhost:5001/log"
MAX_RETRIES = 3
RETRY_DELAY = 1

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def post_with_retry(url, json_data):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, json=json_data, timeout=3)
            response.raise_for_status()
            logger.info(f"Logged message: {json_data['message']}")
            return True
        except Exception as e:
            logger.error(f"Attempt {attempt} failed: {e}")
            if attempt == MAX_RETRIES:
                return False
            time.sleep(RETRY_DELAY)

@app.route("/", methods=["GET"])
def index():
    return "Facade Service is running!"

@app.route("/message", methods=["GET"])
def get_message():
    try:
        response = requests.get(MESSAGES_SERVICE_URL, timeout=3)
        response.raise_for_status()
        message = response.json().get("message", "No message")
        success = post_with_retry(LOGGING_SERVICE_URL, {"message": message})
        if not success:
            return jsonify({"error": "Failed to log message after retries"}), 500
        response = make_response(jsonify({"message": message}))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/message", methods=["POST"])
def post_message():
    try:
        data = request.get_json(silent=True)  # Змінено force_silent на silent
        if not data or "message" not in data:
            return jsonify({"error": "Invalid or missing 'message' in JSON"}), 400
        message = data["message"]
        success = post_with_retry(LOGGING_SERVICE_URL, {"message": message})
        if not success:
            return jsonify({"error": "Failed to log message after retries"}), 500
        response = make_response(jsonify({"status": "Message logged", "message": message}))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except Exception as e:
        logger.error(f"POST error: {str(e)}")
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(port=5000)