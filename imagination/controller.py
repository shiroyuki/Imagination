# v2
from .debug           import get_logger, dump_meta_container
from .loader          import Loader
from .meta.container  import Container, Entity, Factorization, Lambda
from .meta.definition import ParameterCollection
from .wrapper         import Wrapper


class Controller(object):
    def __init__(self,
                 metadata : Container,
                 core_get : callable,
                 transformer_cast : callable
                 ):
        self.__metadata         = metadata
        self.__core_get         = core_get
        self.__transformer_cast = transformer_cast
        self.__logger           = get_logger('controller/{}'.format(metadata.id))

        self.__container_instance = None  # Cache
        self.activation_sequence  = None  # Activation Sequence

    @property
    def metadata(self):
        return self.__metadata

    def activated(self):
        return self.__container_instance is not None

    def activate(self):
        if self.activated():
            return self.__container_instance

        new_instance = self.__instantiate_container()

        if self.__metadata.cacheable:
            self.__container_instance = new_instance

        return new_instance

    def __instantiate_container(self):
        metadata       = self.__metadata
        params         = self.__cast_to_params(self.__metadata.params)
        container_type = type(metadata)
        make_method    = None

        if container_type is Lambda:
            return Loader(metadata.fq_callable_name).package

        if container_type is Entity:
            make_method = Loader(metadata.fqcn).package
        elif container_type is Factorization:
            factory_service = self.__core_get(metadata.factory_id)
            make_method     = getattr(factory_service, metadata.factory_method_name)

        if not make_method:
            raise NotImplementedError('No make method for {}'.format(container_type.__name__))

        new_instance = make_method(*params['sequence'], **params['items'])

        if metadata.interceptions:
            return Wrapper(self.__core_get, new_instance, metadata.interceptions)

        return new_instance

    def __cast_to_params(self, params : ParameterCollection):
        return {
            'sequence': [
                self.__transformer_cast(item)
                for item in params.sequence()
            ],
            'items': {
                key: self.__transformer_cast(value)
                for key, value in params.items()
            },
        }
