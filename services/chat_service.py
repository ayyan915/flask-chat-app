from repositories.chat_repository import save_message_in_db, get_chat_history, get_users
from datetime import datetime
def send_message_service(sender, reciver, message, time):
    save_message_in_db(sender, reciver, message, time)

def get_chat_history_service(sender, reciver):
    messages = get_chat_history(sender, reciver)
    chat_list = []
    for row in messages:
        chat_list.append({
            "id": row[0],
            "sender": row[1],
            "reciver": row[2],
            "message": row[3],
            "send_at": row[4]
        })
    return chat_list

def send_user_dic(username):
    user_list = get_users()
    user_dic = []
    for u in user_list:
        if u[0] != username:
            user_dic.append({
                "username": u[0]
            })
    return user_dic
