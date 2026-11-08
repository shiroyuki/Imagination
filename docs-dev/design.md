# Imagination -- Design & Architecture

This document explains how the pieces of **Imagination** relate to each other.
The diagrams below are written in [Mermaid](https://mermaid.js.org/), which
renders on GitHub and in most Mermaid-aware Markdown viewers.

> **Status of the two approaches.** The **standalone container** and the
> **`@registered` decorator** are the *recommended* way to use Imagination. The
> **XML configuration** approach and **aspect-oriented programming (AOP)**
> interception are *legacy support*: they still work but are marked `@deprecated`
> in the source and are not used by the recommended path. Nothing legacy is
> removed -- it is retained for backward compatibility and documented here.

## 1. Public entry points

The package exposes a small surface (see `imagination/__init__.py`):

| Symbol | Origin | Purpose |
| --- | --- | --- |
| `service` (`registered`) | `imagination.decorator.service` | Declare a class as a service. |
| `container` | `imagination.standalone` | The shared, ready-to-use core. |
| `use(type)` | `imagination.standalone` | Typed shortcut for `container.get(type)`. |

## 2. High-level architecture

```mermaid
graph TD
    subgraph PublicAPI["Public API (imagination package)"]
        USE["use(t) / container.get(id)"]
        REG["@registered()  -- decorator/service"]
        CONT["container  (Imagination, standalone)"]
    end

    subgraph Meta["Metadata  (meta/)"]
        CONTAINER["Container"]
        ENTITY["Entity"]
        FACT["Factorization"]
        LAMBDA["Lambda"]
        PCOL["ParameterCollection / DataDefinition"]
        INTERC["Interception  -- deprecated"]
        MCall["MethodCall"]
        CONTAINER --> ENTITY
        CONTAINER --> FACT
        CONTAINER --> LAMBDA
        CONTAINER --> PCOL
        CONTAINER --> INTERC
        CONTAINER --> MCall
    end

    subgraph Core["Runtime core"]
        IMG["Imagination (core)"]
        CTRL["Controller"]
        TR["Transformer  (helper/transformer)"]
        LOAD["Loader"]
        WRAP["Wrapper / InterceptableCallable  -- AOP, deprecated"]
        IMG --> CTRL
        IMG --> TR
        CTRL --> LOAD
        CTRL --> CONTAINER
        CTRL --> WRAP
        INTERC -. drives .- WRAP
    end

    subgraph AssemblerLegacy["Assembler -- legacy XML path"]
        ASM["Assembler"]
        XMLP["XMLParser  -- deprecated"]
        CR["EntityCreator / FactorizationCreator / LambdaCreator"]
        ASM --> XMLP
        XMLP --> CR
        CR --> CONTAINER
        CR --> INTERC
        ASM --> IMG
    end

    USE --> CONT
    CONT --> IMG
    USE --> REG
    REG -. defines .- IMG
    ASM --> CONT
```

## 3. Definition time -- how `@registered` builds a definition

When a class is decorated, the decorator turns the constructor and the explicit
`params` into metadata on the shared container. It does **not** instantiate the
service.

```mermaid
sequenceDiagram
    participant D as @registered()
    participant C as Imagination (core)
    participant DC as DefinitionContext
    participant SP as set_parameter
    participant PC as ParameterCollection / DataDefinition
    participant M as meta.Container (Entity)

    D->>C: define_entity(id, fqcn) | update_definition(id)
    C->>DC: yield DefinitionContext(core, metadata)
    D->>SP: for each param in params
    SP->>DC: set_param / add_dependency / add_classinfo
    DC->>PC: DataDefinition(kind, value, name)
    PC->>M: metadata.params
    Note over C,M: No service instance is created yet
```

Key relationships:

- `registered` (decorator/service.py) computes the service ID with the default
  strategy `fully_qualified_class_name` (helper/id_naming.py) and then calls
  `Imagination.define_entity` / `update_definition`.
- Those are context managers that yield a `DefinitionContext`
  (helper/context.py); the decorator feeds each configured parameter through
  `set_parameter` (decorator/helper.py), which routes to
  `DefinitionContext.set_param` / `add_dependency` / `add_classinfo`.
- All of this only mutates a `meta.Container` (here an `Entity`); instantiation
  is deferred until the first request.

## 4. Request time -- activation flow of `get()` / `use()`

`use(ServiceClass)` and `container.get(ServiceClass)` share the same path. On the
first request the core locks down, builds the interception graph, computes the
activation sequence, and activates every dependency before the requested one.

```mermaid
sequenceDiagram
    participant U as User
    participant C as Imagination.get()
    participant I as Controller
    participant INST as instantiator (Loader / factory method)
    participant T as Transformer
    participant W as Wrapper (AOP)

    U->>C: get(DataService) / use(DataService)
    C->>C: first request: lock_down + build interception graph
    C->>C: calculate activation sequence
    loop each dependency (and the requested id)
        C->>I: activate(previously_activated)
        I->>INST: instantiate(params)
        INST-->>I: raw instance
        I->>T: cast params + auto-wire by type hints
        T-->>I: cast args / kwargs
        opt has interceptions
            I->>W: wrap(instance, interceptions)
        end
        I->>I: run_initial_calls()
    end
    C-->>U: instance (cached when cacheable)
```

Notes:

- The **instantiator** differs by container type (`Controller.instantiator`):
  - `Entity` -> `Loader(fqcn).package` (loader.py)
  - `Factorization` -> a method on the factory service
  - `Lambda` -> `Loader(fq_callable_name).package`
- **Auto-wiring** (`__scan_for_usable_parameters`) matches constructor parameters
  to registered services by type hint; `Transformer.cast` resolves entity
  references, environment variables, and primitive/collection values.
- **AOP** only happens when a service has interceptions: the raw instance is
  wrapped by `Wrapper` / `InterceptableCallable` (wrapper.py) so that
  *before/after/error* callbacks run without touching the object.

## 5. Metadata class hierarchy

```mermaid
classDiagram
    class Container {
        +string id
        +ParameterCollection params
        +list interceptions
        +list initial_calls
        +bool cacheable
        +bool auto_wired
        +set dependencies
    }
    class Entity {
        +string fqcn
    }
    class Factorization {
        +string factory_id
        +string factory_method_name
    }
    class Lambda {
        +string fq_callable_name
    }
    class Interception {
        <<deprecated>>
        +string when_to_intercept
        +string intercepted_id
        +string method_to_intercept
        +string interceptor_id
        +string intercepting_method
    }
    class ParameterCollection {
        +add(meta, name)
        +sequence()
        +items()
    }
    class DataDefinition {
        +definition
        +name
        +kind
        +transformation_required
    }
    class MethodCall {
        +actor_id
        +method_name
        +parameters
    }

    Container <|-- Entity
    Container <|-- Factorization
    Container <|-- Lambda
    Container o-- ParameterCollection
    Container o-- Interception
    Container o-- MethodCall
    ParameterCollection *-- DataDefinition
```

## 6. Modern vs. legacy

```mermaid
flowchart TD
    M["Modern (recommended)"] --> M1["@registered() decorator"]
    M1 --> M2["DefinitionContext -> meta.Container"]
    M2 --> M3["core.get() / use()"]
    M3 --> M4["Controller -> Wrapper (only when AOP is used)"]

    L["Legacy (deprecated)"] --> L1["XML configuration file"]
    L1 --> L2["Assembler -> XMLParser"]
    L2 --> L3["*Creator -> meta.Container + Interception"]
    L3 --> L4["core.update_metadata()"]
    L4 --> M3
```

The two approaches converge on the **same runtime core** (`Imagination` /
`Controller`). The only difference is *how the metadata is produced*:

- **Modern**: `@registered` builds the metadata in Python via `DefinitionContext`.
- **Legacy**: `Assembler` + `XMLParser` parse an XML file and produce the same
  `meta.Container` / `Interception` objects via the `*Creator` handlers.

## 7. What is marked `@deprecated`

The legacy surface is marked with a compatibility decorator
(`imagination/decorator/deprecated.py`) that re-exports the standard-library
`@deprecated` on Python 3.13+ and is a no-op "dummy" on older Python, so the
legacy code keeps working on every still-supported version:

- `imagination.wrapper.Wrapper` and `imagination.wrapper.InterceptableCallable`
  (AOP runtime) -- decorated at runtime.
- `imagination.meta.definition.Interception` (AOP metadata) -- decorated at
  runtime.
- `imagination.assembler.xml.XMLParser` (XML path) -- documented as deprecated
  (`.. deprecated::` in the docstring); it is not decorated at runtime because it
  is instantiated on the modern default path, where a runtime warning would be
  misleading.

Per the project's `AGENTS.md`, none of this is removed: the legacy modules are
retained and clearly documented.
