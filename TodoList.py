Todo = []

while True:
    print("""
        1. Add Todo
        2. Delete Todo 
        3. View Todo
        4. Edit Todo
        5. Clear all
        #. Exit
    """)
    
    choice = input("Choice: ") 
    if choice == '1':
        item = input("Item: ").strip().title()
        Todo.append(item)
        print(Todo)

    elif choice == '2':
        print(Todo)
        
        
        item = input('Item: ').strip().title()
        if item in Todo:
            confirm = input("Proceed (yes/no): ").strip().lower()
            if confirm == 'yes':
                Todo.remove(item)
                print(f"{item} removed from Todo.")
            else: 
                print("Operation terminated")
        else: 
            print(f"{item} is not in the Todo")
    

    elif choice == '3':
        print(Todo)

    elif choice == '4':
        print(Todo)
        oldtask = input("Task to edit: ").strip().title()
        if oldtask in Todo:           
            ind = Todo.index(oldtask)
            Todo.pop(ind)
            newtask = input("Input New Task: ").strip().title()
            Todo.insert(ind, newtask)
            print("Your New Todo List",Todo)

        else:
            print("Item not in Todo List", Todo)



    elif choice == '5':
        Todo.clear()
        print(Todo)    

    elif choice == '#': 
        print('Bye..')
        exit()
    
    else:
        print("Invalid Option")