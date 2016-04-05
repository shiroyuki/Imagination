from kotoba.kotoba import Kotoba
from imagination.decorator.validator import restrict_type
from imagination.meta.package        import Parameter

class ParameterParsingMixin(object):
    @restrict_type(Kotoba)
    def _get_params(self, node):
        package = Parameter()

        index = 0

        for param in node.children('param'):
            try:
                assert param.attribute('name')\
                    and param.attribute('type'),\
                    'The parameter #{} does not have either name or type.'.format(index)
            except AssertionError as e:
                raise IncompatibleBlockError(e.message)

            index += 1
            name   = param.attribute('name')

            if name in package.kwargs:
                raise DuplicateKeyWarning('There is a parameter name "{}" with that name already registered.'.format(name))
                pass

            package.kwargs[name] = self._transformer.cast(
                param,
                param.attribute('type')
            )

        return package
