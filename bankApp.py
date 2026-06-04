# OOP + SQL

# bank application
# account table - id, fullname, email, password, account_no, balance, created_at
from random import choice, randint

from pwinput import pwinput
import bcrypt

import mysql.connector as sql


class Config:
    __conn = None

    def __init__(self):
        self.__conn = sql.connect(
            host="127.0.0.1", user="root", password="", port="3306", database="mar2026"
        )

        self.__conn.autocommit = True
        self.mycursor = self.__conn.cursor()

    def register(self, fullname, email, password):
        if fullname == "" or email == "" or password == "":
            return "All fields are required. Try again"

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        account_no = randint(2000000000, 2099999999)
        query = "INSERT INTO user_table (fullname, email, password, account_no) VALUES (%s ,%s ,%s ,%s)"
        values = (fullname, email, hashed, account_no)
        self.mycursor.execute(query, values)
        return "Registration Successful"

    def set_password(self):
        password1 = pwinput()
        password2 = pwinput(prompt="Confirm Password: ")

        if password1 != password2:
            print("\nPassword does not match\n")
            return self.set_password()

        return password1

    def login(self, email, password):
        if email == "" or password == "":
            return "All fields are required. Try again"

        query = "SELECT * FROM user_table WHERE email=%s"
        values = (email,)
        self.mycursor.execute(query, values)
        user = self.mycursor.fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user[4].encode("utf-8")):
            print("Login Successful")
            return {
                "fullname": user[1],
                "email": user[2],
                "password": user[4],
                "account_no": user[6],
                "balance": user[7],
            }
        else:
            return "Invalid email or password"


class BankApp(Config):
    def __init__(self):
        super().__init__()
        self.current_user = None

    def menu(self):
        print("""
            
            1. Sign in
            2. Sign up
            #. Exit
        """)

        choice = input("Choice: ")
        if choice == "1":
            self.signin()
        elif choice == "2":
            self.signup()
        elif choice == "#":
            exit()
        else:
            print("Invalid Choice")
            self.menu()

    def signup(self):
        fullname = input("Fullname: ").strip().title()
        email = input("email: ").strip().lower()
        password = self.set_password()
        response = self.register(fullname, email, password)
        print(response)
        self.menu()

    def signin(self):
        email = input("email: ").strip().lower()
        password = pwinput("Insert Password: ")
        user = self.login(email, password)

        if type(user) == dict:
            self.current_user = user
            print(f"Welcome back {user['fullname']}")
            self.dashboard()

        else:
            print("Invalid Credentials")
            self.menu()

    def dashboard(self):
        print("""
        1. Deposit
        2. Withdraw
        3. Check Balance
        4. Transfer
        5. Transaction History
        6. Change Password
        #. Back to Menu
        """)
        choice = input("Choice: ")

        if choice == "1":
            self.deposit()

        elif choice == "2":
            self.withdraw()

        elif choice == "3":
            self.check_balance()

        elif choice == "4":
            self.bk_transfer()

        elif choice == "5":
            self.trans_history()

        elif choice == "6":
            self.pw_change()

        elif choice == "#":
            self.menu()

        else:
            print("Invalid..")
            self.dashboard()

    def trans_store(
        self,
        account_no,
        transact_type,
        transact_amount,
        sender_account_no,
        recipient_account_no,
    ):
        query = "INSERT INTO transact_table (account_no, transact_type, transact_amount, sender_account_no, recipient_account_no) Values(%s,%s,%s,%s,%s)"
        values = (
            self.current_user["account_no"],
            transact_type,
            transact_amount,
            sender_account_no,
            recipient_account_no,
        )
        self.mycursor.execute(query, values)

    def deposit(self):
        amount = float(input("Amount: "))
        if amount < 0:
            print("Invalid amount")
        else:
            new_balance = self.current_user["balance"] + amount
            query = "UPDATE user_table SET balance =%s WHERE email =%s"
            values = (new_balance, self.current_user["email"])
            self.mycursor.execute(query, values)
            self.current_user["balance"] = new_balance
            print(f"Deposit successful. New balance is {new_balance}")

            transact_type = "Deposit"
            transact_amount = amount
            sender_account_no = self.current_user["account_no"]
            recipient_account_no = self.current_user["account_no"]
            self.trans_store(
                self.current_user["account_no"],
                transact_type,
                transact_amount,
                sender_account_no,
                recipient_account_no,
            )

        self.dashboard()

    def withdraw(self):
        amount = float(input("Amount: "))
        if amount < 0:
            print("Invalid amount")

        elif amount > self.current_user["balance"]:
            print("Insufficient fund")

        else:
            print(f"Are you sure you want to withdraw {amount} from your account")
            choice = input("Yes or No: ").strip().lower()

            if choice == "yes":
                new_balance = self.current_user["balance"] - amount
                query = "UPDATE user_table SET balance =%s WHERE email =%s"
                values = (new_balance, self.current_user["email"])
                self.mycursor.execute(query, values)
                self.current_user["balance"] = new_balance
                print(f"Withdrawal successful. New balance is #{new_balance}")

                transact_type = "Withdrawal"
                transact_amount = amount
                sender_account_no = self.current_user["account_no"]
                recipient_account_no = self.current_user["account_no"]
                self.trans_store(
                    self.current_user["account_no"],
                    transact_type,
                    transact_amount,
                    sender_account_no,
                    recipient_account_no,
                )

            else:
                print("Withdraw Terminated")

        self.dashboard()

    def check_balance(self):
        print(f"Your Account Balance: #{self.current_user['balance']}")

        self.dashboard()

    def bk_transfer(self):
        amount = float(input("Amount: "))
        recipient_no = int(input("Recipient Account Number: "))

        if amount < 0:
            print("Invalid amount")

        elif amount > self.current_user["balance"]:
            print("Insufficient fund")

        else:
            query = "SELECT * from user_table WHERE account_no =%s"
            values = (recipient_no,)
            self.mycursor.execute(query, values)
            recipient = self.mycursor.fetchone()

            if recipient:
                print(f"Are you sure you want to transfer {amount} to {recipient[1]}")
                choice = input("Yes or No: ").strip().lower()

                if choice == "yes":
                    recipient_balance = recipient[7]
                    new_recipientbalance = recipient_balance + amount
                    query = "UPDATE user_table SET balance =%s WHERE account_no =%s"
                    values = (new_recipientbalance, recipient_no)
                    self.mycursor.execute(query, values)
                    recipient = new_recipientbalance

                    new_balance = self.current_user["balance"] - amount
                    query = "UPDATE user_table SET balance =%s WHERE email =%s"
                    values = (new_balance, self.current_user["email"])
                    self.mycursor.execute(query, values)
                    self.current_user["balance"] = new_balance

                    print(f"Transfer successful. New balance is #{new_balance}")

                    transact_type = "Transfer"
                    transact_amount = amount
                    sender_account_no = self.current_user["account_no"]
                    recipient_account_no = recipient_no
                    self.trans_store(
                        self.current_user["account_no"],
                        transact_type,
                        transact_amount,
                        sender_account_no,
                        recipient_account_no,
                    )
                else:
                    print("Transfer Terminated")

            else:
                print("Account number does not exist")

        self.dashboard()

    def trans_history(self):
        query = "SELECT * from transact_table WHERE account_no =%s"
        values = (self.current_user["account_no"],)
        self.mycursor.execute(query, values)
        user_history = self.mycursor.fetchall()

        if not user_history:
            print("No transaction history found")

        for history in user_history:
            print(
                f"on the {history[6]}, A {history[2]} of {history[3]} was made by {history[4]} to {history[5]}"
            )

        self.dashboard()

    def pw_change(self):
        print("Changing password")
        old_pw = pwinput("Insert Previous password: ")

        if bcrypt.checkpw(
            old_pw.encode("utf-8"), self.current_user["password"].encode("utf-8")
        ):
            new_pw = self.set_password()

            hashed = bcrypt.hashpw(new_pw.encode("utf-8"), bcrypt.gensalt())
            query = "UPDATE user_table SET password =%s WHERE email =%s"
            values = (hashed, self.current_user["email"])
            self.mycursor.execute(query, values)
            self.current_user["password"] = hashed
            print("Password has been changed")
        else:
            print("Password Incorrect")

        self.dashboard()


bk = BankApp()
bk.menu()
