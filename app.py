from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

app = Flask(__name__)

# Setup Flask session
app.config['SECRET_KEY'] = "Don't tell anyone"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['user_db']
users = db['users']

# Route to render the login form
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in MongoDB
        user = users.find_one({"username": username})

        if user and check_password_hash(user['password'], password):
            # User authenticated, store session
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return "Invalid username or password", 403

    return render_template('login.html')

# Route to render the profile page (only accessible after login)
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('profile.html', username=session['username'])

# Helper function to create a new user (you can call this via a separate registration route)
def create_user(username, password):
    hashed_password = generate_password_hash(password)
    users.insert_one({'username': username, 'password': hashed_password})

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
