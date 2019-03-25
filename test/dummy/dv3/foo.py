from imagination import service


@service.registered(auto_wired=True)
class Foo(object):
    def __init__(self):
        pass