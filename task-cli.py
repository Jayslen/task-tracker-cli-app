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
        self.id = value[-1]["id"] + 1

    def create_task(self, name):
        return {
            "id": self.id,
            "task": name,
            "status": "todo",
            "created_at": f"{datetime.now()}",
            "updated_at": f"{datetime.now()}",
        }

    def preloop(self):
        if not os.path.exists("tasks.json"):
            with open("tasks.json", "w") as file:
                file.write("[]")
        else:
            with open("tasks.json", "r") as f:
                self.update_tasks(json.load(f))

    def postloop(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

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

    def do_show_tasks(self, line):
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


if __name__ == "__main__":
    MyCLI().cmdloop()
