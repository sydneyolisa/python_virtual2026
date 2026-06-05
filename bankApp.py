# OOP + SQL

# bank application
# account table - id, fullname, email, password, account_no, balance, created_at
from random import randint
import re

from pwinput import pwinput
import bcrypt

import mysql.connector as sql


class Config:
    _conn = None

    def __init__(self):
        self._conn = sql.connect(
            host="127.0.0.1", user="root", password="", port="3306", database="mar2026"
        )

        self.mycursor = self._conn.cursor(dictionary=True)

    def register(self, fullname, email, password):
        if fullname == "" or email == "" or password == "":
            return "All fields are required. Try again"

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        account_no = randint(2000000000, 2099999999)
        query = "INSERT INTO user_table (fullname, email, password, account_no) VALUES (%s ,%s ,%s ,%s)"
        values = (fullname, email, hashed, account_no)

        try:
            self.mycursor.execute(query, values)
            self._conn.commit()
            return "Registration Successful"
        except sql.Error as e:
            self._conn.rollback()
            print(f"Database error: {e}")

            return

    def validate_email(self):
        while True:
            email = input("email: ").strip().lower()
            pattern = r"^[\w.-]+@[\w.-]+\.\w{2,}$"
            if not re.match(pattern, email):
                print("Invalid email format")
            else:
                return email

    def set_password(self):
        while True:
            password1 = pwinput()
            password2 = pwinput(prompt="Confirm Password: ")

            if password1 != password2:
                print("\nPassword does not match\n")

            else:
                return password1

    def login(self, email, password):
        if email == "" or password == "":
            return "All fields are required. Try again"

        query = "SELECT * FROM user_table WHERE email=%s"
        values = (email,)

        try:
            self.mycursor.execute(query, values)
            user = self.mycursor.fetchone()

        except sql.Error as e:
            print(f"Database error: {e}")
            return

        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            print("Login Successful")
            return {
                "fullname": user["fullname"],
                "email": user["email"],
                "password": user["password"],
                "account_no": user["account_no"],
                "balance": user["balance"],
            }
        else:
            return "Invalid email or password"


class BankApp(Config):
    def __init__(self):
        super().__init__()
        self.current_user = None

    def menu(self):
        while True:
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

    def signup(self):
        fullname = input("Fullname: ").strip().title()
        if fullname.lower() == "back":
            return

        email = self.validate_email()
        password = self.set_password()
        response = self.register(fullname, email, password)
        print(response)
        return

    def signin(self):
        email = input("email: ").strip().lower()
        if email == "back":
            return
        password = pwinput("Insert Password: ")
        user = self.login(email, password)

        if type(user) == dict:
            self.current_user = user
            print(f"Welcome back {user['fullname']}")
            self.dashboard()

        else:
            print("Invalid Credentials")
            return

    def dashboard(self):
        while True:
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
                return

            else:
                print("Invalid..")

    def trans_store(
        self,
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

        try:
            self.mycursor.execute(query, values)

        except sql.Error as e:
            print(f"Database error: {e}")
            return

    def deposit(self):
        while True:
            try:
                amount = float(input("Amount: ").replace(",", ""))
                break
            except ValueError:
                print("Invalid amount format. Numbers only.")

        if amount < 0:
            print("Invalid amount")
        else:
            new_balance = self.current_user["balance"] + amount
            query = "UPDATE user_table SET balance =%s WHERE email =%s"
            values = (new_balance, self.current_user["email"])

            try:
                self.mycursor.execute(query, values)
                self.current_user["balance"] = new_balance
                print(f"Deposit successful. New balance is {new_balance}")

                transact_type = "Deposit"
                transact_amount = amount
                sender_account_no = self.current_user["account_no"]
                recipient_account_no = self.current_user["account_no"]
                self.trans_store(
                    transact_type,
                    transact_amount,
                    sender_account_no,
                    recipient_account_no,
                )
                self._conn.commit()

            except sql.Error as e:
                self._conn.rollback()
                print(f"Database error: {e}. Deposit Failed")
                return

        return

    def withdraw(self):
        while True:
            try:
                amount = float(input("Amount: ").replace(",", ""))
                break
            except ValueError:
                print("Invalid amount format. Numbers only.")

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

                try:
                    self.mycursor.execute(query, values)
                    self.current_user["balance"] = new_balance
                    print(f"Withdrawal successful. New balance is #{new_balance}")

                    transact_type = "Withdrawal"
                    transact_amount = amount
                    sender_account_no = self.current_user["account_no"]
                    recipient_account_no = self.current_user["account_no"]
                    self.trans_store(
                        transact_type,
                        transact_amount,
                        sender_account_no,
                        recipient_account_no,
                    )
                    self._conn.commit()

                except sql.Error as e:
                    self._conn.rollback()
                    print(f"Database error: {e}. Withdraw reversed")
                    return

            else:
                print("Withdraw Terminated")

        return

    def check_balance(self):
        print(f"Your Account Balance: #{self.current_user['balance']}")

        return

    def bk_transfer(self):
        while True:
            try:
                amount = float(input("Amount: ").replace(",", ""))

                recipient_no = int(input("Recipient Account Number: "))
                break
            except ValueError:
                print("Invalid amount format. Numbers only.")

        if amount < 0:
            print("Invalid amount")

        elif amount > self.current_user["balance"]:
            print("Insufficient fund")

        else:
            query = "SELECT * from user_table WHERE account_no =%s"
            values = (recipient_no,)

            try:
                self.mycursor.execute(query, values)
                recipient = self.mycursor.fetchone()

            except sql.Error as e:
                print(f"Database error: {e}")
                return

            if recipient:
                print(
                    f"Are you sure you want to transfer {amount} to {recipient['fullname']}"
                )
                choice = input("Yes or No: ").strip().lower()

                if choice == "yes":
                    try:
                        recipient_balance = recipient["balance"]
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

                        transact_type = "Transfer"
                        transact_amount = amount
                        sender_account_no = self.current_user["account_no"]
                        recipient_account_no = recipient_no
                        self.trans_store(
                            transact_type,
                            transact_amount,
                            sender_account_no,
                            recipient_account_no,
                        )
                        print(f"Transfer successful. New balance is #{new_balance}")
                        self._conn.commit()

                    except sql.Error as e:
                        self._conn.rollback()
                        print(
                            f"Database error: {e}. Transfer Failed and has been Reversed"
                        )
                        return

                else:
                    print("Transfer Terminated")

            else:
                print("Account number does not exist")

        return

    def trans_history(self):
        query = "SELECT * FROM transact_table WHERE account_no = %s ORDER BY created_at DESC LIMIT 10"
        values = (self.current_user["account_no"],)

        try:
            self.mycursor.execute(query, values)
            user_history = self.mycursor.fetchall()

        except sql.Error as e:
            print(f"Database error: {e}")
            return

        if not user_history:
            print("No transaction history found")

        for history in user_history:
            print(
                f"on the {history['created_at']}, A {history['transact_type']} of {history['transact_amount']} was made by {history['sender_account_no']} to {history['recipient_account_no']}"
            )

        return

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

            try:
                self.mycursor.execute(query, values)
                self.current_user["password"] = hashed
                print("Password has been changed")
                self._conn.commit()

            except sql.Error as e:
                self._conn.rollback()
                print(f"Database error: {e}.Password update failed")
                return
        else:
            print("Password Incorrect")

        return


try:
    bk = BankApp()
    bk.menu()
except KeyboardInterrupt:
    print("\nGoodbye!")
