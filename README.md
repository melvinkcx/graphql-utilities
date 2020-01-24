# graphql-utils

![](https://github.com/melvinkcx/graphql-utils/workflows/tests/badge.svg)

Collection of utils, middleware, decorators for graphql-core>=3.0 (formerly known as graphql-core-next)

## What's included?

* __Depth analysis__: `graphql-utils` provides a configurable custom `ExecutionContext` that 
can be configured to perform depth analysis.
* `@run_only_once` decorator for middleware: each field resolver involves running all middleware. 
For middleware of certain purpose like authenticating users shouldn't have to be run multiple times. 

## Installation

```
pip install graphene-utils
```

Alternatively, if you use pipenv:

```
pipenv install graphene-utils
```

## What's next?

* __Query cost analysis__: <TODO>

## Motivation

In recent projects, I ran into some problems with Graphene including missing document-level (request-level) middleware, etc. 
`graphql-utils` is a compilation of utilities and custom execution context I wrote.

## Contributing

Any form of contribution, feature requests, bug reports, pull requests are largely welcome.  
