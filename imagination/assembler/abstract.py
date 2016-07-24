class ConfigParser(object):
    def can_handle(self, filepath : str): # -> bool
        raise NotImplemented()

    def parse(self, filepath : str):
        raise NotImplemented()
