import json

from Task import Task


class Tasklist(list):
    def __init__(self, filepath=None):
        super().__init__()
        self.filepath = filepath

    def appends(self, tasks):
        for task in tasks:
            self.append(task)

    def get_doable_tasks(self, time):
        self.sort(key=lambda t: t.heuristic(time))

        offers = Tasklist()
        while self:
            task = self.pop()
            if task.heuristic(time) == 0:
                self.append(task)
                break
            else:
                offers.append(task)

        return offers

    def to_json(self):
        res = {}
        tasks = list(map(lambda t: t.to_json(), self))
        res["tasks"] = tasks
        return res

    def write(self):
        if self.filepath is None:
            self.filepath = input("Save to: ")
        with open(self.filepath, 'w') as file:
            file.write(json.dumps(self.to_json(), indent=4))

    @staticmethod
    def read(filepath):
        with open(filepath) as file:
            content = json.load(file)
            tasklist = Tasklist(filepath)
            tasks = map(Task.from_json, content["tasks"])
            tasklist.appends(tasks)
            return tasklist

    def __repr__(self):
        res = "path: {}, tasks: ".format(self.filepath)
        res += ", ".join(map(lambda t: t.__repr__(), self))
        return res
