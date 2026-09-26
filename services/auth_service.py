from werkzeug.security import generate_password_hash, check_password_hash
from repositories.auth_repository import register_user_in_db, get_user_detail_from_db
from flask_jwt_extended import create_access_token

def register_user_service(username, password):
    user_detail = get_user_detail_from_db(username)
    if user_detail:
        return "user already exists"
    hash_pass = generate_password_hash(password)
    register_user_in_db(username, hash_pass)
    return None


def login_user_service(username, password):
    userpass = get_user_detail_from_db(username)
    if not userpass:
        return None, "user not exists"
    if check_password_hash(userpass, password):
        token = create_access_token(identity=username)
        return token, None
    else:
        return None, "check password and try again"
