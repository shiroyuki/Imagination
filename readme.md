from imagination.decorator.service import registered

# Imagination

## Basic Usage

Let's take a look at this example.

Suppose we have two services, `DataService` and `DataAdapter`, where `DataService` requires `DataAdapter`.

```python
class DataAdapter:
    ...


class DataService:
    def __init__(self, adapter: DataAdapter):
        ...
    ...
```

Traditionally, to instantiate `DataService`, you need to do this somewhere in your code.

```python
adapter = DataAdapter()
service = DataService(adapter)
```

Now, with **Imagination**, first you will need to annotate/decorate the classes.

```python
from imagination.decorator.service import registered

@registered()
class DataAdapter:
    ...

@registered()
class DataService:
    ...
```

Here is what just happened.
* **Imagination** understands how to instantiate an instance of both classes.
* However, it **DOES NOT** instantiate any registered classes.
  * By design, it instantiates when needed.

And then, you can fetch the reference `DataService` by running this.

```python
from imagination.standalone import container, use

container.get(DataService).do_something(...)  # since v3.3
use(DataService).do_something(...)  # since v3.4
```

Where the framework will instantiate `DataAdapter` first and then `DataService` as `DataService` requires `DataAdapter`.

> While both `container.get` and `use` yield the same result, the `use` method is preferable if you are using an IDE.

## Detailed Documentation

The documentation is available at http://readthedocs.org/docs/imagination/.
