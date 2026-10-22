# Imagination

## Basic Usage

Imagination is a dependency injection framework for Python. Its standalone container
can register services with decorators and inject constructor dependencies without XML.

Suppose `DataService` requires a `DataAdapter`. Register both classes, then retrieve
the service with `use()`:

```python
from __future__ import annotations

from imagination.decorator.service import registered
from imagination.standalone import use


@registered()
class DataAdapter:
    def fetch(self) -> str:
        return "Hello from Imagination"


@registered()
class DataService:
    def __init__(self, adapter: DataAdapter):
        self.adapter = adapter

    def do_something(self) -> str:
        return self.adapter.fetch()


service = use(DataService)
assert service.do_something() == "Hello from Imagination"
assert use(DataService) is service
```

`@registered()` declares a singleton service without instantiating it. On the first
request, Imagination creates `DataAdapter` and injects it into `DataService` using
the constructor's type hint. Subsequent requests reuse the same instances. Import
the modules containing decorated classes before requesting services.

`use(ServiceClass)`, available since v3.4, returns the same instance as
`container.get(ServiceClass)`. Its generic return type helps IDEs and type checkers
infer the service type:

```python
from imagination.standalone import container

assert container.get(DataService) is service
```

## Configuring Dependencies

Required constructor arguments annotated with registered service classes are wired
automatically. Supply primitive values through the decorator's `params` argument:

```python
from imagination.decorator.config import Parameter


@registered(params=[Parameter("Panda", name="name")])
class NamedDataService:
    def __init__(self, name: str, adapter: DataAdapter):
        self.name = name
        self.adapter = adapter


assert use(NamedDataService).name == "Panda"
```

Use `Service` from `imagination.decorator.config` for explicit service references
by class or ID, including injecting a subclass into a parameter annotated with its
base class. Parameters with default values keep their defaults unless explicitly
configured.

Postponed annotations (`from __future__ import annotations`) are supported for
auto-wiring and runtime type checks. Referenced types must be resolvable in the
module where the constructor is defined.

The standalone container also loads existing XML configuration files from
`IMAGINATION_CONF_FILEPATH`, `imagination.xml`, and `services.xml`, in that order.
The latter two paths are relative to the current working directory.

## Detailed Documentation

See the [standalone mode and decorator guide](docs/source/getting-started/10-standalone_mode.rst)
for parameter options and service IDs, or browse the
[full documentation](https://imagination.readthedocs.io/).
