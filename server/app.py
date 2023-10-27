from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages_list = []
        messages = Message.query.all()
        for n in messages:
            messages_list.append(n.to_dict())

        return make_response(messages_list, 200)
    
    elif request.method == "POST":
        post_content = request.get_json()
        new_message = Message(
            body=post_content["body"],
            username=post_content["username"]
        )

        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()

    if message == None:
        response_body = {
            "message": f"Message #{id} can't be found."
        }
        return make_response(response_body, 404)
    elif request.method == "GET":
        return make_response(message.to_dict(), 200)
    elif request.method == "PATCH":
        patch_content = request.get_json()
        for attr in patch_content:
            setattr(message, attr, patch_content[attr])
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(), 200)
        
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "deleted": True,
            "message": f"Message #{id} has been deleted."
        }
        return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555)
