from database import get_db
from model import Messages, Users
from sqlalchemy import or_


def save_message_in_db(sender, reciver, message, time):
    db = get_db()

    try:
        new_message = Messages(
            sender=sender,
            reciver=reciver,
            message=message,
            send_at=time
        )

        db.add(new_message)
        db.commit()

    finally:
        db.close()


def get_chat_history(sender, reciver):
    db = get_db()

    try:
        chat_history = db.query(Messages).filter(
            or_(
                (Messages.sender == sender) &
                (Messages.reciver == reciver),

                (Messages.sender == reciver) &
                (Messages.reciver == sender)
            )
        ).order_by(Messages.send_at).all()

        return chat_history

    finally:
        db.close()


def get_users():
    db = get_db()

    try:
        users_list = db.query(Users).all()

        return users_list

    finally:
        db.close()