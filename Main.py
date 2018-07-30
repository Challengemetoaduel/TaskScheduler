import re

from Task import Task
from Tasklist import Tasklist


class Cmd:
    def __init__(self):
        self.tasklist = None
        self.running = False
        self.unsaved_changes = False
        self.offers = []

        self.commands = \
            [
                ("help", "\t\tPrint this help."),
                ("new", "\t\t\tCreate a new todo list."),
                ("load", "\t\tLoad a saved todo list."),
                ("add", "\t\t\tAdd a new task to the current todo list."),
                ("la", "\t\t\tList all tasks in current list."),
                ("calc", "\t\tCalculate all doable tasks."),
                ("lo", "\t\t\tList calculated tasks."),
                ("complete", "\tComplete a task from the calculated tasks."),
                ("save", "\t\tSave all changes to the current list."),
                ("exit", "\t\tClose task scheduler.")]

        self.cmd_dict = {
            "add": self.add,
            "exit": self.exit,
            "new": self.new,
            "save": self.save,
            "lo": self.list_offers,
            "la": self.list_all,
            "calc": self.calculate,
            "load": self.load,
            "complete": self.complete,
            "help": self.help
        }

    def start(self):
        self.running = True
        self.loop()

    def new(self):
        if self.unsaved_changes:
            save = self.prompt("Save unsaved changes? [Y/n]")
            if save:
                self.save()

        self.unsaved_changes = True
        self.tasklist = Tasklist()

    def complete(self):
        if not self.offers:
            print("No offers to mark completed.")
        else:
            self.list_offers()
            ind = int(input("Competed: ")) -1
            if ind < 0 or ind >= len(self.offers):
                print("No offer with index {}.".format(ind+1))
            else:
                self.offers.pop(ind)



    def load(self):
        if self.unsaved_changes:
            save = self.prompt("Save unsaved changes? [Y/n]")
            if save:
                self.save()
        filepath = input("Load from: ")
        self.tasklist = Tasklist.read(filepath)


    def list_offers(self):
        if not self.offers:
            print("No offers yet.")
        else:
            l = len(self.offers)
            zipped = zip(range(1, l+1), self.offers)
            print("\n".join(["{}: {}".format(i, t) for i, t in zipped]))

    def list_all(self):
        if self.tasklist is None:
            new = self.prompt("Start new tasklist? [Y/n]")
            if new:
                self.new()
            return
        if self.tasklist:
            print("\n".join(map(lambda t: t.__str__(), self.tasklist)))
        else:
            print("No tasks.")

    def calculate(self):
        if self.tasklist is None:
            new = self.prompt("Start new tasklist? [Y/n]")
            if new:
                self.new()
            return
        time_line = input("Available time: ")
        time = self.parse_time(time_line)
        self.offers = self.tasklist.get_doable_tasks(time)
        if self.offers:
            self.unsaved_changes = True
        self.list_offers()



    def exit(self):
        self.tasklist.appends(self.offers)
        if self.unsaved_changes:
            save = self.prompt("Save unsaved changes? [Y/n]")
            if save:
                self.save()
        self.running = False

    def nothing(self):
        print("Unknown command. Use \"help\" to print known commands")
        pass

    def help(self):
        for cmd, description in self.commands:
            print("{}{}".format(cmd, description))

    def loop(self):
        while self.running:
            cmd = input("> ")
            func = self.cmd_dict.get(cmd, self.nothing)
            func()

    def add(self):
        if self.tasklist is None:
            new = self.prompt("Start new tasklist? [Y/n]")
            if new:
                self.new()
            return

        self.unsaved_changes = True
        name = input("Name: ")
        time = self.parse_time(input("Duration: "))
        self.tasklist.append(Task(name, time))

    @staticmethod
    def parse_time(line):
        time_reg = "(?:(?P<hours>\d+):(?P<mins>\d\d)h?|(?P<cnt>\d+)(?P<unit>[dhm]))"
        time_match = re.fullmatch(time_reg, line)
        if time_match is None:
            print("Invalid time input. Defaulting to 10m.")
            return 10
        elif time_match.group("hours"):
            hours = int(time_match.group("hours"))
            mins = int(time_match.group("mins"))
            return hours * 60 + mins
        elif time_match.group("cnt"):
            cnt = int(time_match.group("cnt"))
            multiplier = {"d": 24 * 60, "h": 60, "m": 1}[time_match.group("unit")]
            return cnt * multiplier


    def prompt(self, text):
        while True:
            answer = input(text).lower()
            if answer in ["", "y", "yes"]:
                return True
            elif answer in ["n", "no"]:
                return False

    def save(self):
        self.tasklist.write()
        self.unsaved_changes = False

if __name__ == '__main__':
    Cmd().start()