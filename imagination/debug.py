import pprint


class PrintableMixin(object):
    def __repr__(self):
        classinfo = type(self)
        props     = dir(self)
        exported  = []
        fqcn      = classinfo.__name__

        if classinfo.__module__:
            fqcn = '{}.{}'.format(classinfo.__module__, fqcn)

        for prop_name in props:
            if prop_name[0] == '_':
                continue

            prop = getattr(self, prop_name)

            if callable(prop):
                continue

            exported.append('{}="{}"'.format(prop_name, prop))

        if not exported:
            return '<{}>'.format(fqcn)

        return '<{} {}>'.format(fqcn, ' '.join(exported))

def dump_meta_container(metadata):
    params = metadata.params
    data = {
        'id': metadata.id,
        'type': metadata.kind,
        'class': metadata.fqcn,
        'dependencies': metadata.dependencies,
        'params': {
            'sequence': [ i for i in params.sequence() ],
            'items': { k: v for k, v in params.items() },
        },
    }

    pprint.pprint(data, indent = 2)
