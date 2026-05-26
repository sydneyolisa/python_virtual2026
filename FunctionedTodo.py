Todo = []

def home():

    print(Todo)
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
        addTodo()

    elif choice == '2':
        delTodo()

    elif choice == '3':
        viewTodo()

    elif choice == '4':
        editTodo()

    elif choice == '5':
        clearTodo()

    elif choice == '#':
        exit()

    else:
        print("Invalid Option")


def addTodo():
    item = input("Item: ").strip().title()
    Todo.append(item)
    print(Todo)
    home()

def delTodo():
    print(Todo)
            
    item = input('Item: ').strip().title()
    if item in Todo:
        confirm = input("Proceed (yes/no): ").strip().lower()
        if confirm == 'yes':
            Todo.remove(item)
            print(Todo)
            print(f"{item} removed from Todo.")
        else: 
            print("Operation terminated")
    else: 
        print(f"{item} is not in the Todo")
    #i should add a way for this to loop back even if user inputs an item not found , instead of taking it back to home

    
    home()

def viewTodo():
    print(Todo)
    home()   

def editTodo():
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
    #i should add a way for edit to loop back even if user inputs an item not found , instead of taking it back to home


    home()    

def clearTodo():
    #I should add logic asking user to confirm if the want to really clear todo
    Todo.clear()
    print(Todo) 
    home()


home()    
