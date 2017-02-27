class DummyException(Exception):
    """ Dummy Exception """
    def __init__(self, previous_error, positional_parameters, keyword_parameters, *args, **kwargs):
        Exception.__init__(self,*args,**kwargs)

        self.previous_error        = previous_error
        self.positional_parameters = positional_parameters
        self.keyword_parameters    = keyword_parameters

class Alpha(object):
    def init_self_destruction_1(self):
        raise RuntimeError('panda one')

    def init_self_destruction_2(self, a, b, c, d = None, e = None):
        raise RuntimeError('panda two')

class Bravo(object):
    def handle_error(self, previous_error, positional_parameters, keyword_parameters):
        raise DummyException(previous_error, positional_parameters, keyword_parameters)
