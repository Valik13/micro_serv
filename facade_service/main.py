from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

MESSAGES_SERVICE_URL = "http://localhost:5002/message"
LOGGING_SERVICE_URL = "http://localhost:5001/log"

MAX_RETRIES = 3       # макс кількість спроб
RETRY_DELAY = 1       # затримка між спробами (сек)

def post_with_retry(url, json_data):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, json=json_data, timeout=3)
            response.raise_for_status()  # кине виключення при помилках HTTP
            return True
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == MAX_RETRIES:
                return False
            time.sleep(RETRY_DELAY)


@app.route("/", methods=["GET"])
def index():
    return "Facade Service is running!"


@app.route("/message", methods=["GET"])
def get_message():
    try:
        response = requests.get(MESSAGES_SERVICE_URL)
        message = response.json().get("message", "No message")

        # Відправляємо повідомлення в logging-service з retry
        success = post_with_retry(LOGGING_SERVICE_URL, {"message": message})

        if not success:
            return jsonify({"error": "Failed to send message to logging-service after retries"}), 500

        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)