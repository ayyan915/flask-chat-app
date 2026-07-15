from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, render_template, jsonify
from services.chat_service import send_user_dic

chat = Blueprint("chat", __name__)
@chat.route("/chat")
@jwt_required(locations=["cookies"])
def show_chat():
    return render_template("chat.html")


@chat.route("/users")
@jwt_required(locations=["cookies"])
def get_users():
    username = get_jwt_identity()
    dic = send_user_dic(username)
    print(username)
    return jsonify(dic)