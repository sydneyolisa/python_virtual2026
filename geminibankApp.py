import mysql.connector as sql
import bcrypt
from random import randint
from pwinput import pwinput

class Config:
    def __init__(self):
        # Database connection
        self.conn = sql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            port="3306",
            database="mar2026",
            autocommit=True
        )
        self.mycursor = self.conn.cursor(dictionary=True) # dictionary=True makes results easier to handle

    def register(self, fullname, email, password):
        if not all([fullname, email, password]):
            return "All fields are required."
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        account_no = randint(2000000000, 2099999999)
        
        try:
            query = "INSERT INTO user_table (fullname, email, password, account_no, balance) VALUES (%s, %s, %s, %s, %s)"
            self.mycursor.execute(query, (fullname, email, hashed, account_no, 0.0))
            return "Registration Successful!"
        except sql.Error as e:
            return f"Error: {e}"

    def login_user(self, email, password):
        query = "SELECT * FROM user_table WHERE email=%s"
        self.mycursor.execute(query, (email,))
        user = self.mycursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
        return None

class BankApp(Config):
    def __init__(self):
        super().__init__()
        self.current_user = None # This tracks who is logged in

    def set_password(self):
        p1 = pwinput("Password: ")
        p2 = pwinput("Confirm Password: ")
        if p1 != p2:
            print("\nPasswords do not match. Try again.")
            return self.set_password()
        return p1

    def menu(self):
        print("\n--- WELCOME TO BANK ---")
        print("1. Sign in\n2. Sign up\n#. Exit")
        choice = input("Choice: ")
        if choice == "1": self.signin()
        elif choice == "2": self.signup()
        elif choice == "#": exit()
        else: self.menu()

    def signup(self):
        fn = input("Fullname: ").strip().title()
        em = input("Email: ").strip().lower()
        pw = self.set_password()
        print(self.register(fn, em, pw))
        self.menu()

    def signin(self):
        em = input("Email: ").strip().lower()
        pw = pwinput("Password: ")
        user = self.login_user(em, pw)
        if user:
            self.current_user = user
            print(f"\nWelcome, {user['fullname']}!")
            self.dashboard()
        else:
            print("Invalid credentials.")
            self.menu()

    def dashboard(self):
        print(f"\n--- DASHBOARD ---")
        print("1. Deposit\n2. Withdraw\n3. Check Balance\n#. Logout")
        choice = input("Choice: ")

        if choice == '1': self.deposit()
        elif choice == '2': self.withdraw()
        elif choice == '3': self.check_balance()
        elif choice == '#': self.menu()
        else: self.dashboard()

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        if amount > 0:
            new_balance = self.current_user['balance'] + amount
            query = "UPDATE user_table SET balance=%s WHERE email=%s"
            self.mycursor.execute(query, (new_balance, self.current_user['email']))
            self.current_user['balance'] = new_balance # Update local state
            print(f"Successfully deposited. New Balance: {new_balance}")
        else:
            print("Invalid amount.")
        self.dashboard()

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        if 0 < amount <= self.current_user['balance']:
            new_balance = self.current_user['balance'] - amount
            query = "UPDATE user_table SET balance=%s WHERE email=%s"
            self.mycursor.execute(query, (new_balance, self.current_user['email']))
            self.current_user['balance'] = new_balance
            print(f"Withdrawal successful. New Balance: {new_balance}")
        else:
            print("Insufficient funds or invalid amount.")
        self.dashboard()

    def check_balance(self):
        print(f"\nAccount Holder: {self.current_user['fullname']}")
        print(f"Current Balance: {self.current_user['balance']}")
        self.dashboard()

bk = BankApp()
bk.menu()