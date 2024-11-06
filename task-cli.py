import cmd
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box

task_done = "done"
task_in_progress = "in progress"
task_todo = "todo"
tasks_status = [task_done, task_in_progress, task_todo]


class MyCLI(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.id = 0

    prompt = ">>"
    intro = "Welcome to track list CLI app, write help, to get all the commands"

    def update_tasks(self, value):
        self.tasks = value
        try:
            self.id = value[-1]["id"] + 1
        except IndexError:
            None

    def update_file(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def create_task(self, name):
        return {
            "id": self.id,
            "task": name.lower(),
            "status": task_todo.lower(),
            "created_at": f"{datetime.now()}",
            "updated_at": f"{datetime.now()}",
        }

    def search_task(self, list, id: int, first, last):
        if type(id) is not int:
            return None

        if first > last:
            return None

        midpoint = (first + last) // 2

        if midpoint >= len(list):
            return None

        if list[midpoint]["id"] == id:
            return midpoint
        elif list[midpoint]["id"] > id:
            return self.search_task(list, id, first, midpoint - 1)
        else:
            return self.search_task(list, id, midpoint + 1, last)

    def update_status(self, id, status):
        try:
            selected_task_index = self.search_task(
                first=0, last=len(self.tasks), id=int(id), list=self.tasks
            )
            if selected_task_index is None:
                print("There is no task with that id, try with other one")
            else:
                self.tasks[selected_task_index]["status"] = status
                self.tasks[selected_task_index]["updated_at"] = f"{datetime.now()}"
                self.update_file()
                print(
                    f"Task {self.tasks[selected_task_index]['task'].upper()} mark as {status}"
                )
        except ValueError:
            print("Id not valid, must be a number")
            return None

    def preloop(self):
        if not os.path.exists("tasks.json"):
            with open("tasks.json", "w") as file:
                file.write("[]")
        else:
            with open("tasks.json", "r+") as f:
                try:
                    self.update_tasks(json.load(f))
                except json.JSONDecodeError:
                    f.write("[]")

    def postloop(self):
        self.update_file()

    def do_help(self, line):
        console = Console()
        console.print(
            "You can perform certaint actions with these commands \n help: Get all the commands \n add_task: Add a task \n show_tasks: show all task saved \n delete {id} delete a task providing the id of it \n update {id} new name: Edit a taks"
        )

    def do_quit(self, line):
        return True

    def do_add(self, line):
        new_task = self.create_task(line)
        self.tasks.append(new_task)
        self.id = self.tasks[len(self.tasks) - 1]["id"] + 1
        self.update_file()
        print(f"Task {line.upper()} added")

    def do_list(self, line):
        tasks_to_show = []
        task_txt = ""
        if line.strip() not in tasks_status or len(line.strip()) == 0:
            print("Showing all the tasks")
            tasks_to_show = self.tasks
        else:
            tasks_to_show = [x for x in self.tasks if x["status"] == line]
            task_txt = line

        if len(self.tasks) == 0:
            print("No tasks to show")
            return None

        rows = [list(x.values()) for x in tasks_to_show]
        columns = list(self.tasks[0].keys())

        table = Table(title=f"Tasks {task_txt}", show_lines=True, box=box.DOUBLE_EDGE)
        console = Console()

        for x in columns:
            table.add_column(x)

        for x in rows:
            row = list(x)
            row[0] = str(row[0])
            row[1] = row[1].capitalize()
            row[2] = row[2].capitalize()
            table.add_row(*row, style="magenta")

        console.print(table)

    def do_delete(self, line):
        try:
            selected_task_index = self.search_task(
                first=0, last=len(self.tasks), id=int(line), list=self.tasks
            )
            if selected_task_index is None:
                print("There is no task with that id, try with other one")
            else:
                print(f"Task {self.tasks[selected_task_index]['task'].upper()} deleted")
                self.tasks.pop(selected_task_index)
                self.update_file()
        except ValueError:
            print("Id not valid, must be a number")
            return None

    def do_mark_in_progress(self, line):
        self.update_status(id=line, status=task_in_progress)

    def do_mark_done(self, line):
        self.update_status(id=line, status=task_done)

    def do_update(self, line):
        task_id, *description = line.split(" ")
        selected_task_index = None
        try:
            selected_task_index = self.search_task(
                first=0, last=len(self.tasks), id=int(task_id), list=self.tasks
            )
            if selected_task_index is None:
                print("There is no task with that id, try with other one")
            else:
                None
                self.tasks[selected_task_index]["task"] = " ".join(description)
                self.update_file()
                print(f"Task {task_id} updated")
        except ValueError:
            print("Id not valid, must be a number")
            return None


if __name__ == "__main__":
    MyCLI().cmdloop()
