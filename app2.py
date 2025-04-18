from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import openai
import os

# Import from auth module
from auth import auth as auth_blueprint, db, login_manager

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# CORS Configuration (for local + deployed frontend)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:3000", "https://travel-ai-frontend.onrender.com"]}})

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# App config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import User model for login manager
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprint for auth routes
app.register_blueprint(auth_blueprint)

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Create database tables
with app.app_context():
    db.create_all()

# --------------------------- Custom Routes --------------------------- #

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


@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.json
    if not data.get("user_id") or not data.get("ticket_id"):
        return jsonify({"error": "Missing required parameters"}), 400

    return jsonify({
        "message": "Ticket booked successfully!",
        "ticket_id": data["ticket_id"]
    })


# --------------------------- Run the App --------------------------- #

if __name__ == '__main__':
    app.run(debug=True)
