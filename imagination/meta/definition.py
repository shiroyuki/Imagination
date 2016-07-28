# v2
from ..debug import PrintableMixin


class DuplicateParameterDefinitionWarning(Warning):
    """ Warning for Duplicate Parameter Definition """


class DataDefinition(PrintableMixin):
    def __init__(self, definition, name : str = None, kind : str = None, transformation_required : bool = True):
        self.__name       = name
        self.__kind       = kind or 'str'
        self.__definition = definition

        self.__transformation_required = transformation_required

    @property
    def name(self):
        return self.__name

    @property
    def kind(self):
        return self.__kind

    @property
    def definition(self):
        return self.__definition

    @property
    def transformation_required(self):
        return self.__transformation_required


class ParameterCollection(PrintableMixin):
    def __init__(self):
        self.__list = list()
        self.__map  = dict()

    @property
    def all(self):
        return {
            'sequence': [i for i in self.sequence()],
            'items': {k: v for k, v in self.items()},
        }

    def sequence(self):
        for item in self.__list:
            yield item

    def items(self):
        for k, v in self.__map.items():
            yield k, v

    def add(self, meta_parameter : DataDefinition, name = None):
        if not name:
            self.__list.append(meta_parameter)

            return

        if name in self.__map:
            raise DuplicateParameterDefinitionWarning(name)

        self.__map[name] = meta_parameter

    def __len__(self):
        return len(self.__list) + len(self.__map)
