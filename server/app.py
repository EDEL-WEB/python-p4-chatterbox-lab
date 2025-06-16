from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate

from server.models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# ✅ GET /messages - return all messages sorted by created_at ASC
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

# ✅ POST /messages - create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    try:
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201
    except KeyError:
        return jsonify({"error": "Missing body or username"}), 400

# ✅ PATCH /messages/<id> - update body of a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)  # ✅ Updated
    if not message:
        return jsonify({"error": "Message not found"}), 404

    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
        db.session.commit()
    
    return jsonify(message.to_dict()), 200

# ✅ DELETE /messages/<id> - delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)  # ✅ Updated
    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return '', 204  # No content

if __name__ == '__main__':
    app.run(port=5555)
