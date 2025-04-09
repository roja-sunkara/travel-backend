from flask import Flask, request, jsonify
import requests
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your actual API keys
TRAVEL_API_KEY = "your_travel_api_key"
OPENAI_API_KEY = "your_openai_api_key"
client = OpenAI(api_key=OPENAI_API_KEY)

# Search Tickets
@app.route('/search_tickets', methods=['GET'])
def search_tickets():
    source = request.args.get('source')
    destination = request.args.get('destination')
    date = request.args.get('date')

    if not source or not destination or not date:
        return jsonify({"error": "Missing required parameters"}), 400

    results = [
        {"details": f"Bus from {source} to {destination} on {date} - Rs.500"},
        {"details": f"Train from {source} to {destination} on {date} - Rs.350"},
    ]
    return jsonify({"results": results})

# Book Ticket
@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.json

    if not data.get("user_id") or not data.get("ticket_id"):
        return jsonify({"error": "Missing required parameters"}), 400

    return jsonify({
        "message": "Ticket booked successfully!",
        "ticket_id": data["ticket_id"]
    })

# Chatbot (OpenAI)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print("Chatbot error:", e)
        return jsonify({"error": "Chatbot failed."}), 500

# Search for available hotels
@app.route('/search_hotels', methods=['GET'])
def search_hotels():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Missing required parameter: city"}), 400

    # Simulated hotel data
    dummy_hotels = {
        "vijayawada": [
            {"name": "Hotel Ilapuram", "price": 1800},
            {"name": "Midtown Hotel", "price": 2200}
        ],
        "chennai": [
            {"name": "Taj Club House", "price": 4500},
            {"name": "The Park Chennai", "price": 3900}
        ]
