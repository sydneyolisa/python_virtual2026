while True:


    print("Smart Calculator") 

    x = int(input("Enter value: "))

    while True: 
        print("""
            Input the sign of operation you want to perform:
                1. Addition(+)
                2. Subtraction(-)
                3. Division(/)  
                4. Mulpilication(*)
                5. Result(=)
                6. Final Result(#)
        """)
        sign = input("Sign: ").strip()

        if sign == "+" :
            y = int(input("Enter next value: "))
            z = x + y
            print(z)
            x = z

        elif sign == "-" :
            y = int(input("Enter next value: "))
            z = x - y
            print(z)
            x = z

        elif sign == "/" :
            y = int(input("Enter next value: "))
            z = x / y
            print(z)
            x = z

        elif sign == "*" :
            y = int(input("Enter next value: "))
            z = x * y
            print(z)
            x = z

        elif sign == "=" :
            
            print(x)   
             

        elif sign == "#":
            
            print(x) 
            break 

        else:
            print('Input just the Sign of the operation') 
        



