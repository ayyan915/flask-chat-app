from database import get_db
from model import Users


def get_user_detail_from_db(username):
    db = get_db()

    try:
        user = db.query(Users).filter(
            Users.name == username
        ).first()

        if user:
            return user.password

        return None

    finally:
        db.close()


def register_user_in_db(username, password):
    db = get_db()

    try:
        new_user = Users(
            name=username,
            password=password
        )

        db.add(new_user)
        db.commit()

    finally:
        db.close()