db = []

def home():
    print("""
            1. Sign Up
            2. Sign In
            #. Exit
    """)

    option = input("What do you want to do? Ans:").strip()
    
    if option == "1":
        signUp()

    elif option == "2":
        signIn()

    elif option == "#":
        exit()

    else:
        print("Invalid Option")
        home()

def signUp():
    print("Sign Up")
    fullname = input("Fullname: ").strip().title()

    while True:
        email = input("Email: ").strip().lower()
        if email.find('@') == -1:
            print("Invalid Email.Try again")
            continue

        if any(user["Email"] == email for user in db):
            print("Email already Exists.Try again.") 


        print("Email Accepted")
        break
        
        

    while True:
        Password = input("Password: ").strip()
        if len(Password) < 8:
            print("Password needs at least 8 characters. Try again.")
        else:
            print("Password Accepted")
            break  

    db.append({"Fullname": fullname,
                "Email": email,
                "Password": Password
                })
    print("Registration Successful")
    menu()


def signIn():
    print("Sign In")

    email = input("Email: ").strip().lower()
    if email.find('@') == -1:
            print("Invalid Email.Try again")
            signIn()
    
    Password = input("Password: ").strip()
    if len(Password) < 8:
            print("Password needs at least 8 characters. Try again.")
            signIn()
    

    if any(user["Email"] == email and user["Password"] == Password for user in db):
            print("Login Successful.") 
            menu()
    else: 
        print("Invalid password/Email")
        home()

balance = 0

def menu():
    print(f"""
        Account Balance: #{balance}  

        1. Deposit
        2. Withdraw
        3. Check balance 
        #. Exit 
    """)
    
    choice = input("Choice: ")
    if choice == '1':
        deposit()
        
    elif choice == '2':
        withdraw()
    
    elif choice == '3':
        checkBalance()
        
    
    elif choice == "#":
        home()
    
    else:
        print("Invalid..")
        menu()
    
def deposit():
    global balance
    
    amount = float(input("Amount: "))
    if amount < 0:
        print("Invalid amount")  
    else:
        balance += amount
        print("Deposit successfull")
        
    menu()
    
def withdraw():
    global balance
    
    amount = float(input("Amount: "))
    if amount < 0:
        print("Invalid amount") 
    
    elif amount > balance:
        print("Insufficient fund")
    
    else:
        balance -= amount
        print("withdrawal successful")
        
    menu()

def checkBalance():
    global balance  
    
    print(f"Your Account Balance: #{balance}")
    menu()
home()