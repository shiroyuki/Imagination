class StrategyController(object):
    def __init__(self, name : str, strategy_mapping : dict, strategy_order : list, settings : dict):
        self.name     = name
        self.settings = settings

        self.strategy_mapping = strategy_mapping
        self.strategy_order   = strategy_order

class Strategy(object):
    def __init__(self, name : str):
        self.name = name
