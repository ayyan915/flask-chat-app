from database import db

def save_message_in_db(sender, reciver, message, time):
    con = db()
    cursor = con.cursor()
    cursor.execute("insert into messages(sender, reciver, message, send_at) values(?, ?, ?, ?)", (sender, reciver, message, time,))
    con.commit()
    con.close()
    

def get_chat_history(sender, reciver):
    con = db()
    cursor = con.cursor()
    cursor.execute("select * from messages where (sender = ? and reciver = ?) or (sender = ? and reciver = ?) order by send_at", (sender, reciver, reciver, sender))
    chat_history = cursor.fetchall()
    con.close()
    return chat_history

def get_users():
    con = db()
    cursor = con.cursor()
    cursor.execute("select name from users")
    users_list = cursor.fetchall()
    return users_list