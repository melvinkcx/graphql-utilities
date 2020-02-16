.. _query_cost_analysis:

Using Query Cost Analysis
=========================

The most exciting part of this library is query cost analysis. It calculates the complexity of queries received and halt execution if the complexity exceeds the permitted value.


Step 1: Build Schema with Cost Directive
----------------------------------------

First, you need a `custom GraphQL directive <http://spec.graphql.org/June2018/#sec-Language.Directives>`_: `@cost()` provided by the library.

You can:

1. **import them from `graphql-utilities`**, then create a schema along with the directive.

    .. code-block:: python

        from graphql import build_schema
        from graphql_utilities import cost_directive_source_doc

        build_schema(source=cost_directive_source_doc + """
            type Post @cost(complexity: 5) {
                postId: ID!
                title: String
            }
        """)

2. or **use a helper function `build_schema_with_cost()`**:

    .. code-block:: python

        from graphql_utilities import build_schema_with_cost

        build_schema_with_cost(source="""
            type Post @cost(complexity: 5) {
                postId: ID!
                title: String
            }
        """)

`build_schema_with_cost()` is a wrapper of `graphql.build_schema()`.
It stitches the **cost directive** with your schema before invoking `build_schema()`.
Hence, the function signature of `graphql_utilities.build_schema_with_cost()` is exactly the same as `graphql.build_schema()`:

.. literalinclude:: ../graphql_utilities/utilities.py
   :language: python
   :linenos:
   :lines: 8-13

.. include:: ./query_cost_analysis_basic_usage.rst

Step 3: Enable Cost Analysis
-----------------------------

To enable cost analysis, you must use the `ExtendedExecutionContext` provided by the library.

All you need to do are:

1. Pass `graphql_utilities.ExtendedExecutionContext` as the value of `execution_context_class` into any of `graphql.graphql_sync()`, `graphql.graphql()`, or `graphql.execute()`
2. Pass the following `context_value`:

    .. code-block:: python

        {"cost_analysis": {
           "max_complexity": 5   # Maximum complexity allowed
        }}

Example:
^^^^^^^^^
.. code-block:: python

    from graphql_utilities import ExtendedExecutionContext, build_schema_with_cost

    schema = build_schema_with_cost(source="""
        type Post @cost(complexity: 5) {
            postId: ID!
            title: String   @cost(complexity: 20)
        }

        type Query {
            post(postId: ID!): Post
        }
    """)

    query = """
        {
            post(postId: "XXXXX") {
                postId
                title
            }
        }
    """

    results = graphql_sync(schema=schema,
                        source=query,
                        execution_context_class=ExtendedExecutionContext,
                        context_value={
                            "cost_analysis": {
                                "max_complexity": 8
                            }
                        })

    results # ExecutionResult(data=None, errors=[GraphQLError("25 exceeded max complexity of 8")])


Advanced Usage
---------------

For more advanced usage of query cost analysis, refer to :ref:`query_cost_analysis_advanced_usage`.