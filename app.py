from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
next_id = 1

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

# GET single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# CREATE user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email required"}), 400
    
    user = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"]
    }
    users[next_id] = user
    next_id += 1
    return jsonify(user), 201

# UPDATE user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify(user), 200

# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
