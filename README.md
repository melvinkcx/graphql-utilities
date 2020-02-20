# graphql-utilities

![](https://github.com/melvinkcx/graphql-utilities/workflows/tests/badge.svg)

**graphql-utilities** tries to secure your GraphQL API from malicious queries and provides utilities to make using `graphql-core` easier.

1. It comes with a custom configurable `ExtendedExecutionContext` class that is capable of performing:

   * **query cost analysis**: define the cost of your queries using the `@cost()` directive provided, `graphql-utilities` provides helper functions and custom execution context to protect you from overly complex queries.
   * **depth limiting**: limit the maximum depth of queries, it's especially useful with object types with recursive relationship

2. It also ships decorators for:

   * **resource-level/one-shot middleware**: middleware in `graphql-core` is run at field-level, it is handly when you need your middleware to run only once, especially auth-related middleware.

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
graphql_sync(schema=schema, source=query,
               context_value={"depth_analysis": {
                   "max_depth": 2   # Maximum depth allowed
               }},
               execution_context_class=ExtendedExecutionContext     # Use the `ExtendedExecutionContext` provided in `graphql-utilities`
        )
```

### Query Cost Analysis

See the documentation at [https://graphql-utilities.readthedocs.io/en/latest/](https://graphql-utilities.readthedocs.io/en/latest/)

## Motivation

In recent projects, I ran into some problems with `graphene` and `graphql-core` including missing operation-level middleware (See [issue here](https://github.com/graphql-python/graphene/issues/1117)), etc. 
`graphql-utilities` is a compilation of utilities and custom execution context for depth analysis, etc targeting `graphql-core>=3.0`.

## Contributing

Any form of contribution, feature requests, bug reports, pull requests are largely welcome.  

## Licenses

MIT Licensed. GraphQL logo is licensed under Facebook [BSD](http://opensource.org/licenses/bsd-license.php).