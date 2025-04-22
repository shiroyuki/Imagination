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
from imagination.standalone import of

of(DataService).do_something(...)
```

## Detailed Documentation

The documentation is available at http://readthedocs.org/docs/imagination/.
