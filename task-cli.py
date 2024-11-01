import cmd
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table


class MyCLI(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.tasks = []

    prompt = ">>"
    intro = "Welcome to track list CLI app, write help, to get all the commands"

    def update_tasks(self, value):
        self.tasks = value

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


if __name__ == "__main__":
    MyCLI().cmdloop()
