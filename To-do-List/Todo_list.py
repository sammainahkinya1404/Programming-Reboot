def main():
    print("Welcome to our To-Do List!")
    tasks = []  # Initialize an empty list to store tasks
    
    while True:  # Loop until the user chooses to exit
        print("\nPlease Select An Operation to Perform:")
        print("1. Add Task to List")
        print("2. Delete Task from List")
        print("3. Mark a Task as Completed")
        print("4. Display All Tasks")
        print("5. Exit")
        
        option = int(input("Enter your choice: "))
        
        if option == 1:
            add(tasks)
        elif option == 2:
            delete_task(tasks)
        elif option == 3:
            mark_completed(tasks)
        elif option == 4:
            view_all(tasks)
        elif option == 5:
            print("Thank you for using our To-Do List!")
            break  # Exit the loop and end the program
        else:
            print("Wrong Option Selected! Please try again.")
  
def add(tasks):
    task = {}  # Create an empty dictionary for the task
    task_name = input("Enter Task Name: ")
    task_body = input("Enter Task Body: ")
    
    task["name"] = task_name
    task["body"] = task_body
    task["completed"] = False  # Default to not completed
    
    tasks.append(task)
    print("Task Added Successfully")

def view_all(tasks):
    if len(tasks) == 0:
        print("No Tasks Found")
    else:
        print("Task List:")
        for idx, task in enumerate(tasks, start=1):
            status = "Completed" if task["completed"] else "Not Completed"
            print(f"{idx}. {task['name']} - {status}")

def delete_task(tasks):
    view_all(tasks)
    if len(tasks) == 0:
        return
    task_num = int(input("Enter the number of the task to delete: "))
    
    if 0 < task_num <= len(tasks):
        tasks.pop(task_num - 1)
        print("Task Deleted Successfully")
    else:
        print("Invalid task number")

def mark_completed(tasks):
    view_all(tasks)
    if len(tasks) == 0:
        return
    task_num = int(input("Enter the number of the task to mark as completed: "))
    
    if 0 < task_num <= len(tasks):
        tasks[task_num - 1]["completed"] = True
        print("Task marked as completed!")
    else:
        print("Invalid task number")

main()
