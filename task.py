import json
import os
import argparse


TASK_FILE = "tasks.json"


parser = argparse.ArgumentParser(description="Task Tracker CLI")
subparsers = parser.add_subparsers(dest="command")

# python task.py add "Buy milk"

add_parser = subparsers.add_parser("add")
add_parser.add_argument("description")

# python task.py update 1 "New description"

update_parser = subparsers.add_parser("update")
update_parser.add_argument("id", type=int)
update_parser.add_argument("description")


delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("id", type=int)


inprogress_parser = subparsers.add_parser("mark-in-progress")
inprogress_parser.add_argument("id", type=int)

done_parser = subparsers.add_parser("mark-done")
done_parser.add_argument("id", type=int)

list_parser = subparsers.add_parser("list")
list_parser.add_argument("status", nargs="?", default="all")


def load_tasks():
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as f:
            json.dump([], f)
    with open(TASK_FILE, "r") as f:
        return json.load(f)


def save_task(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo"
    }
    tasks.append(new_task)
    save_task(tasks)
    print("Task added:", new_task)


def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            save_task(tasks)
            print("Task updated.")
            return
    print("Task not found.")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print("Task not found.")
        return
    save_task(new_tasks)
    print("Task deleted.")


def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            save_task(tasks)
            print("Task marked in progress.")
            return
    print("Task not found.")


def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_task(tasks)
            print("Task marked done.")
            return
    print("Task not found.")


def list_tasks(status):
    tasks = load_tasks()

    if status == "all":
        filtered = tasks
    else:
        filtered = [t for t in tasks if t["status"] == status]

    if not filtered:
        print("No tasks found.")
        return

    for task in filtered:
        print(f"{task['id']}. [{task['status']}] {task['description']}")


args = parser.parse_args()

if args.command == "add":
    add_task(args.description)

elif args.command == "update":
    update_task(args.id, args.description)

elif args.command == "delete":
    delete_task(args.id)

elif args.command == "mark-in-progress":
    mark_in_progress(args.id)

elif args.command == "mark-done":
    mark_done(args.id)

elif args.command == "list":
    list_tasks(args.status)

else:
    parser.print_help()
