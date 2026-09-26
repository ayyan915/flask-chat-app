from database import get_db
from model import Users

db = get_db()

def get_user_detail_from_db(username):
    user = db.query(Users).filter(Users.name == username).first()
    db.close()
    if user:
        return user.password
    
    return None


def register_user_in_db(username, password):
    new_user = Users(
        name=username,
        password=password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()