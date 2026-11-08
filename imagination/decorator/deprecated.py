# MISC: Compatibility shim for the standard-library ``@deprecated`` decorator.
#
# The ``deprecated`` module was added to the standard library in Python 3.13.
# To keep the source compatible with every still-supported Python (the declared
# floor is ``requires-python = ">=3.9"``), this module re-exports the standard
# library decorator on 3.13+ and falls back to a no-op "dummy" decorator on older
# versions, so legacy code marked with ``@deprecated`` still imports and runs
# unchanged.
try:
    from deprecated import deprecated  # noqa: F401  (stdlib, Python >= 3.13)
except ModuleNotFoundError:  # Python < 3.13: no-op dummy decorator
    def deprecated(*args, **kwargs):
        """ No-op fallback for ``@deprecated`` on Python < 3.13.

            Works both as ``@deprecated`` (no parentheses) and as
            ``@deprecated(reason=...)`` / ``@deprecated('...')`` (with arguments).
        """
        # ``@deprecated`` with no arguments: ``args[0]`` is the wrapped object.
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return args[0]

        def _wrap(obj):
            return obj

        return _wrap
