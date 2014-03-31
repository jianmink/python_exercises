import inspect 

class Record:
    def __init__(self, **kw):
        self.__dict__.update(kw)
colors = Record(alarm='red', warning='orange', normal='green')
for each in inspect.getmembers(colors):
    print each

shape = Record(x=10, y=10)
for each in inspect.getmembers(shape):
    print each