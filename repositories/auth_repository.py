from database import db

def get_user_detail_from_db(username):
    con = db()
    cursor = con.cursor()
    cursor.execute("select password from users where name = ?", (username,))
    user_password = cursor.fetchone()
    return user_password



def register_user_in_db(username, password):
    con = db()
    cursor = con.cursor()
    try:
        cursor.execute("insert into users(name, password) values(?, ?)", (username, password))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()