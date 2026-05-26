db = []

while True:
    print("""
            1. Sign Up
            2. Sign In
            #. Exit
    """)

    option = input("What do you want to do? Ans:")

    if option == "1":
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

    elif option == "2":
        print("Sign In")

        email = input("Email: ").strip().lower()
        Password = input("Password: ").strip()

        if any(user["Email"] == email and user["Password"] == Password for user in db):
                print("Login Successful.") 

        else: 
            print("Invalid password/Email")

    elif option == "#":
        exit()

    else:
        print("Invalid Option")