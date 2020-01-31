# graphql-utilities

![](https://github.com/melvinkcx/graphql-utilities/workflows/tests/badge.svg)

Collection of utils, middleware, decorators for graphql-core>=3.0 (formerly known as graphql-core-next)

## What's included?

* __depth analysis__: `graphql-utilities` provides a configurable custom `ExecutionContext` that 
can be configured to perform depth analysis.
* `@run_only_once` decorator for middleware: each field resolver involves running all middleware. 
For middleware of certain purpose like authenticating users shouldn't run multiple times. 

## Installation

```sh
pip install graphql-utilities
```

Alternatively, if you use pipenv:

```sh
pipenv install graphql-utilities
```

## Examples

### Operation-level middleware (One-shot middleware)

```python
from graphql_utilities.decorators import run_only_once


class AuthMiddleware:
    @run_only_once
    def resolve(self, next_, root, info, *args, **kwargs):
        # middleware logic
        return next_(root, info, *args, **kwargs)   
```

### Limiting Query Depth

```python
# import your schema
from graphql import execute, parse   # Requires `graphql-core>=3.0`
from graphql_utilities.execution import ExtendedExecutionContext


query = '{ field_1_str field_2_int field_3_obj { field_3_obj_sub_1 { xxx } } }'
execute(schema=schema, document=parse(query),
               context_value={"depth_analysis": {
                   "max_depth": 2   # Maximum depth allowed
               }},
               execution_context_class=ExtendedExecutionContext     # Use the `ExtendedExecutionContext` provided in `graphql-utilities`
        )
```

## What's next? 

Here is a list of items I am working on: (or will work on):

* Query cost analysis

## Motivation

In recent projects, I ran into some problems with `graphene` and `graphql-core` including missing operation-level middleware (See [issue here](https://github.com/graphql-python/graphene/issues/1117)), etc. 
`graphql-utilities` is a compilation of utilities and custom execution context for depth analysis, etc targeting `graphql-core>=3.0`.

## Contributing

Any form of contribution, feature requests, bug reports, pull requests are largely welcome.  
