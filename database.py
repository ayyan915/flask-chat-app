import sqlite3
def db():
    con = sqlite3.connect("data.db")
    return con
con = db()
cursor = con.cursor()

cursor.execute("""create table if not exists users(
               id integer primary key autoincrement,
               name text unique,
               password text
               )""")
cursor.execute("""create table if not exists messages(
               id integer primary key autoincrement,
               sender text,
               reciver text,
               message text,
               send_at text
               )""")
print("table created")