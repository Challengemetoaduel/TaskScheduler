class Task:
    def __init__(self, name, duration=0):
        self.name = name
        self.duration = duration

    def heuristic(self, available_time=0):
        if self.duration > available_time:
            return 0
        else:
            return self.duration

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(dict):
        return Task(dict["name"], dict["duration"])

    def __repr__(self):
        h, m = divmod(self.duration, 60)
        return "\"{}\": {}:{:02d}".format(self.name, h, m)