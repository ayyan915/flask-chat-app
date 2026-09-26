from flask import Flask, request
from flask_socketio import SocketIO
from routes.auth import auth
from routes.chat import chat
from datetime import datetime
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from services.chat_service import send_message_service, get_chat_history_service
import os
from database import Base, engine
import model
app = Flask(__name__)
Base.metadata.create_all(bind=engine)

app.config["JWT_SECRET_KEY"] = "ayyan2009"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
jwt = JWTManager(app)
socketio = SocketIO(app)

app.register_blueprint(auth)
app.register_blueprint(chat)

online_users = {}
@socketio.on("connect")
def handle_connection():
    verify_jwt_in_request(locations=["cookies"])
    username = get_jwt_identity()
    online_users[username] = request.sid
    user_list = list(online_users.keys())
    socketio.emit("user_status", {
        "username": username,
        "status": "◉"
    })
    socketio.emit("online_user_list", user_list, to=request.sid)
    print(online_users)




@socketio.on("disconnect")
def user_disconnect():
    discon_username = None
    for username, sid in online_users.items():
        if sid == request.sid:
            discon_username = username
            break
    if discon_username:
        online_users.pop(discon_username)
        socketio.emit("user_status", {
            "username": discon_username,
            "status": "○"
        })

@socketio.on("send_message")
def send_message(data):
    verify_jwt_in_request(locations=["cookies"])
    reciver_name = data["to"]
    message = data["message"]
    reciver_id = None
    sender_name = get_jwt_identity()
    sender_id = request.sid
    time = datetime.now().strftime("%d-%m-%y %I-%M-%p")
    send_message_service(sender_name, reciver_name, message, time)

    for username, sid in online_users.items():
        if username == reciver_name:
            reciver_id = sid
            break
    
    if reciver_id:
        socketio.emit("new_message", {
        "sender_name": sender_name,
        "reciver_name": reciver_name,
        "message": message,
        "send_at": time
    }, to=reciver_id)
    if sender_id:
        socketio.emit("new_message", {
        "sender_name": sender_name,
        "reciver_name": reciver_name,
        "message": message,
        "send_at": time
    }, to=sender_id)

@socketio.on("chat_load")
def load_chat(data):
    verify_jwt_in_request(locations=["cookies"])
    reciver = data["reciver"]
    sender = get_jwt_identity()
    messages = get_chat_history_service(sender, reciver)
    socketio.emit("chat_history", messages, to=request.sid)


@socketio.on("typing_to")
def typing_status(data):
    print(data)
    verify_jwt_in_request(locations=["cookies"])
    sender_name = get_jwt_identity()
    reciver_name = data["to"]
    reciver_sid = online_users.get(reciver_name)
    if reciver_sid:
        print(reciver_sid)
        socketio.emit("typing_status", sender_name, to=reciver_sid)

@socketio.on("stop_typing")
def stop_typing(data):
    print(data)
    verify_jwt_in_request(locations=["cookies"])
    sender_name = get_jwt_identity()
    reciver_name = data["to"]
    reciver_id = online_users.get(reciver_name)
    if reciver_id:
        socketio.emit("stop_typing", sender_name, to=reciver_id)

print("app started")
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
    