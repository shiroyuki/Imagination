import sys

def retrieve_module(name):
    if name not in sys.modules:
        __import__(name)

    return sys.modules[name]