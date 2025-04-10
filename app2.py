from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# ✅ Import auth and db from auth.py
from auth import auth_bp, db, login_manager

app = Flask(__name__)
CORS(app)

# ✅ Required configs for login and db
app.config['SECRET_KEY'] = 'your_secret_key_here'  # You can change this to a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize extensions
db.init_app(app)
login_manager.init_app(app)

# ✅ Register auth blueprint
app.register_blueprint(auth_bp)

# ✅ OpenAI API Key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ✅ Create DB tables
with app.app_context():
    db.create_all()

# ===============================
# ✈️ Ticket Search Endpoint
# ===============================
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

# ===============================
# 🏨 Hotel Search Endpoint
# ===============================
@app.route('/search_hotels', methods=['GET'])
def search_hotels():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing required parameter: city"}), 400
    dummy_hotels = {
        "vijayawada": [{"name": "Hotel Ilapuram", "price": 1800}, {"name": "Midtown Hotel", "price": 2200}],
        "chennai": [{"name": "Taj Club House", "price": 4500}, {"name": "The Park Chennai", "price": 3900}],
        "bangalore": [{"name": "The Oberoi", "price": 5500}, {"name": "ITC Gardenia", "price": 5200}]
    }
    hotels = dummy_hotels.get(city.lower(), [])
    return jsonify({"hotels": hotels})

# ===============================
# 🤖 Chatbot Endpoint
# ===============================
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    try:
        response = openai.ChatCompletion.create(
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

# ===============================
# 🎫 Book Ticket Endpoint
# ===============================
@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.json
    if not data.get("user_id") or not data.get("ticket_id"):
        return jsonify({"error": "Missing required parameters"}), 400
    return jsonify({
        "message": "Ticket booked successfully!",
        "ticket_id": data["ticket_id"]
    })

# ===============================
# ✅ Run the app
# ===============================
if __name__ == '__main__':
    app.run(debug=True)




