class ConfigParser(object):
    def can_handle(self, filepath : str) -> bool:
        raise NotImplementedError()

    def parse(self, filepath : str) -> dict:
        raise NotImplementedError()
