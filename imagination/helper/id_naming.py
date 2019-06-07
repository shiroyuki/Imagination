from .general import get_fully_qualified_class_name


def fully_qualified_class_name(cls) -> str:
    return get_fully_qualified_class_name(cls)


def shorten_fully_qualified_class_name(cls) -> str:
    fqcn = fully_qualified_class_name(cls)
    fqcn_segments = fqcn.split('.')
    return '{}.{}'.format(
        '.'.join(s[0].lower() for s in fqcn_segments[:-1]),
        fqcn_segments[-1],
    )


def qualified_class_name_only(cls) -> str:
    return cls.__qualname__


def class_name_only(cls) -> str:
    return cls.__name__
