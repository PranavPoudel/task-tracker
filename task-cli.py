import sys
import json
import os
import datetime

def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    with open("tasks.json", "r") as file:
        return json.load(file)
    
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=2)

def now():
    return datetime.datetime.now().isoformat()    

def add_task(description):
    tasks = load_tasks()
    new_id = max((task["id"] for task in tasks),default=0)+1
    new_date = now()
    new_task = {
                "id" : new_id,
                "description": description,
                "status": "todo",
                "createdAt": now(),
                "updatedAt": now()
            }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added Successfully ID:{new_task['id']}")

def update_tasks(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"]= description
            task["updatedAt"]= now()
            save_tasks(tasks)
            print(f"successfully updated task {task['id']}")
            return 
    print("unsucessful at updating task")
 
def delete_task(task_id):
    tasks = load_tasks()
    for i,task in enumerate(tasks):
        if task['id']== task_id:
            del tasks[i]
            save_tasks(tasks)
            print("task deletion : sucess")
            return
    print("error deleting task: task not found")

def mark_task(task_id, status):
    tasks = load_tasks()
    for i,task in enumerate(tasks):
        if task['id']== task_id:
            task['status']= status
            task['updatedAt']= now()
            print(f"task {task['id']}'s status updated")
            save_tasks(tasks)

def list_task(status_fil = None):
    tasks = load_tasks()
    if status_fil:
        tasks = [t for t in tasks if t['status'] == status_fil]
    if not tasks:
        print("no task found")
        return
    
    print(f"{'ID':<5} | {'Status':<12} | {'Description':<30} | {'Updated At'}")
    print("-" * 70)
    for task in tasks:
        print(f"{task['id']:<5} | {task['status']:<12} | {task['description']:<30} | {task['updatedAt']}")


def main():
    if len(sys.argv) < 2:
        print("usage: python task-cli.py <command> <arguments>")
        sys.exit(1)

    command = sys.argv[1]
    try:
        if command =="add" and len(sys.argv)>2:
            add_task(sys.argv[2])
        
        elif command =="update" and len(sys.argv)>3:
            update_tasks(int(sys.argv[2]),sys.argv[3])
        
        elif command =="delete" and len (sys.argv)>2:
            delete_task(int(sys.argv[2]))

        elif command == "mark" and len (sys.argv) >2:
            mark_task(int(sys.argv[2]),"in-progress")
        elif command == "mark-done" and len (sys.argv) >2:
            mark_task(int(sys.argv[2]),"done")
        elif command == "list":
            status = sys.argv[2] if len(sys.argv) >= 3 else None
            list_task(status)
        else:
            print("Invalid command or missing arguments.")
            print("Commands: add, update, delete, mark-in-progress, mark-done, list [todo|in-progress|done]")
    except ValueError:
        print("error: taskID must be an integer")
    
    except Exception as e:
        print(f"an unexpected error : {e}")




if __name__ == "__main__":
    main()
