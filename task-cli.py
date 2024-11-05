import cmd
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box


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
            "task": name,
            "status": "todo",
            "created_at": f"{datetime.now()}",
            "updated_at": f"{datetime.now()}",
        }

    def search_task(self, list, id, first, last):
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

    def do_add_task(self, line):
        new_task = self.create_task(line)
        self.tasks.append(new_task)
        self.id = self.tasks[len(self.tasks) - 1]["id"] + 1
        self.update_file()
        print(f"Task {line.upper()} added")

    def do_show_tasks(self, line):
        if len(self.tasks) == 0:
            print("No tasks to show")
            return None

        rows = [list(x.values()) for x in self.tasks]
        columns = list(self.tasks[0].keys())

        table = Table(title="Tasks", show_lines=True, box=box.DOUBLE_EDGE)
        console = Console()

        for x in columns:
            table.add_column(x)

        for x in rows:
            row = list(x)
            row[0] = str(row[0])
            row[1] = row[1].capitalize()
            table.add_row(*row, style="magenta")

        console.print(table)

    def do_delete(self, line):
        selected_task = self.search_task(
            first=0, last=len(self.tasks), id=int(line), list=self.tasks
        )
        if selected_task is None:
            print("There is no task with that id, try with other one")
        else:
            print(f"Task {self.tasks[selected_task]['task'].upper()} deleted")
            self.tasks.pop(selected_task)
            self.update_file()


if __name__ == "__main__":
    MyCLI().cmdloop()
