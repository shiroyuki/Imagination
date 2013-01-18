import os
import sys

def retrieve_module(name):
    if name not in sys.modules:
        __import__(name)

    return sys.modules[name]

def retrieve_module_path(name):
    module = retrieve_module(name)

    return os.path.dirname(module.__file__) if module else None