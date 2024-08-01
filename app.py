from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.flask_db
users_collection = db.users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))
    return jsonify(users), 200

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    users_collection.insert_one(data)
    return jsonify({'message': 'User added successfully!'}), 201

@app.route('/user/<string:username>', methods=['PUT'])
def update_user(username):
    data = request.get_json()
    result = users_collection.update_one({'username': username}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'User updated successfully!'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/<string:username>', methods=['DELETE'])
def delete_user(username):
    result = users_collection.delete_one({'username': username})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully!'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
