class Something(object):
    def __init__(self): pass
    def alpha(self): pass
    def bravo(self): pass
    def doubler(self): pass
    def trippler(self): pass

class Ticker(object):
    def __init__(self):
        self.sequence = []

    def tick(self, result):
        self.sequence.append(result)

class Manager(object):
    def getWorkerObject(self, name):
        return Worker(name)

    def getDuplicationMethod(self, multiplier):
        def duplicate(value):
            return value * multiplier

        return duplicate

class Worker(object):
    def __init__(self, name):
        self.name = name

    def ping(self):
        return self.name