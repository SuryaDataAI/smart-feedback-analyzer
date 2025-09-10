from flask import Flask, request, jsonify
from sentiment_model import analyze_sentiment
import json
import os

app = Flask(__name__)

DATA_FILE = "../data/feedback.json"

# Ensure feedback storage exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route('/')
def home():
    return "Smart Feedback Analyzer API is running!"

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = data.get("feedback", "")

    if not feedback:
        return jsonify({"error": "Feedback cannot be empty"}), 400

    sentiment = analyze_sentiment(feedback)

    # Save feedback
    with open(DATA_FILE, "r+") as f:
        feedback_list = json.load(f)
        feedback_list.append({"feedback": feedback, "sentiment": sentiment})
        f.seek(0)
        json.dump(feedback_list, f, indent=4)

    return jsonify({"message": "Feedback received", "sentiment": sentiment})

@app.route('/get_feedback', methods=['GET'])
def get_feedback():
    with open(DATA_FILE, "r") as f:
        feedback_list = json.load(f)
    return jsonify(feedback_list)

if __name__ == '__main__':
    app.run(debug=True)
