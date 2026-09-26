from repositories.chat_repository import (
    save_message_in_db,
    get_chat_history,
    get_users
)


def send_message_service(sender, reciver, message, time):
    save_message_in_db(sender, reciver, message, time)


def get_chat_history_service(sender, reciver):

    messages = get_chat_history(sender, reciver)

    chat_list = []

    for row in messages:

        chat_list.append({
            "id": row.id,
            "sender": row.sender,
            "reciver": row.reciver,
            "message": row.message,
            "send_at": row.send_at
        })

    return chat_list


def send_user_dic(username):

    user_list = get_users()

    user_dic = []

    for u in user_list:

        if u.name != username:

            user_dic.append({
                "username": u.name
            })

    return user_dic