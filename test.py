from database import db
sender = "ali"
reciver = "ali"
con = db()
cursor = con.cursor()
cursor.execute("select * from messages where (sender = ? and reciver = ?) or (reciver = ? and sender = ?) order by send_at desc", (sender, reciver, reciver, sender))
chat_history = cursor.fetchall()
con.close()
print(chat_history)

