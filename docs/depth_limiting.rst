.. _depth_limiting:

Limiting Query Depth
=====================

The `ExtendedExecutionContext` execution context class provided in `graphql-utilities` is capable of limiting the maximum depth of queries, it's especially useful with object types with recursive relationship.

All you need to do are:

1. Pass `graphql_utilities.ExtendedExecutionContext` as the value of `execution_context_class` into any of `graphql.graphql_sync()`, `graphql.graphql()`, or `graphql.execute()`
2. Pass the following `context_value`:

    .. code-block:: python
        {"depth_analysis": {
           "max_depth": 5   # Maximum depth allowed
        }}

Example:
^^^^^^^^^
.. code-block:: python

    from graphql_utilities import ExtendedExecutionContext

    query = """
        {
            posts(first: 5) {
                postId
                author {
                    authorId
                    posts(first: 5) {
                        postId
                        author {
                            authorId
                            posts(first: 5) {
                                postId
                                author {
                                    authorId
                                    posts(first: 5) {
                                        postId
                                        // Depth: 7
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """

    results = graphql_sync(schema=schema,
                        source=query,
                        execution_context_class=ExtendedExecutionContext,
                        context_value={
                            "depth_analysis": {
                                "max_depth": 5
                            }
                        })

    results # ExecutionResult(data=None, errors=[GraphQLError("Reached max depth of 5")])