from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['user_db']
users = db['users']

# Example user data
username = 'user1'
password = 'securepassword'  # This will be hashed

# Hash the password
hashed_password = generate_password_hash(password)

# Insert into the MongoDB collection
users.insert_one({'username': username, 'password': hashed_password})

print(f"User '{username}' inserted successfully.")
