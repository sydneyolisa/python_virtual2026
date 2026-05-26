import mysql.connector as sql
from pwinput import pwinput
from sqlalchemy import true

conn = sql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    port="3306",
    database = "mar2026"
    )

conn.autocommit = True

mycursor = conn.cursor()

# mycursor.execute("DROP DATABASE march2026")
# mycursor.execute("CREATE DATABASE mar2026")
# mycursor.execute("SHOW DATABASES")
# print(mycursor.fetchall())

# mycursor.execute("""
#             CREATE TABLE user_table(
#                 id INT PRIMARY KEY AUTO_INCREMENT,
#                 fullname VARCHAR(50),
#                 email VARCHAR(50) UNIQUE,
#                 password VARCHAR(50),
#                 created_at DATETIME DEFAULT CURRENT_TIMESTAMP                 
#                 )

# """)

# mycursor.execute("ALTER TABLE user_table ADD address VARCHAR(50) AFTER email")

# mycursor.execute("ALTER TABLE user_table CHANGE COLUMN location address VARCHAR(50)")

# mycursor.execute("ALTER TABLE user_table DROP COLUMN address")

#DML

def register():
    print("="*10)
    print("Sign up")
    print("="*10)
    
    fullname = input("Fullname: ").strip().title()
    email = input("email: ").strip().lower()
    address = input("address: ").strip()
    password = pwinput()
    
    query = "INSERT INTO user_table(fullname, email, address, password) VALUES(%s, %s, %s, %s)"
    # values = ('John Smith', "john@gmail.com", 'Lagos', '1234')
    values = (fullname, email, address, password)
    mycursor.execute(query, values)
    # conn.commit()
    print("Registration successful")
    
# register()

# query = "UPDATE user_table SET password=%s WHERE email=%s"
# values = ("12345", "max@gmail.com\\")
# mycursor.execute(query,values)

# query = "DELETE FROM user_table WHERE id=%s"
# value = (2,)
# mycursor.execute(query,value)

# DQL 
# mycursor.execute("SELECT fullname, email, address FROM user_table")
# details = mycursor.fetchall()
# print(details)

# mycursor.execute("SELECT * FROM user_table WHERE id=3")
# details = mycursor.fetchone()
# print(details)

def login():
    email = input("email: ").strip().lower()
    password = pwinput()
    
    query = "SELECT * FROM user_table WHERE email=%s AND password=%s"
    values=(email, password)
    mycursor.execute(query, values)
    details = mycursor.fetchone()
    
    if details:
        print(f"Welcome back {details[1]}")
        
    else:
        print("Invalid email or password")
        
login()