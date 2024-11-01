import cmd
import json
import os


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


if __name__ == "__main__":
    MyCLI().cmdloop()
