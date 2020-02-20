.. _query_cost_analysis_advanced_usage:

Advanced Usage of Query Cost Analysis
=====================================

Basic complexity calculation may be insufficient. `graphql-utilities` cost analysis also supports:

* :ref:`complexity multiplier <complexity_multiplier>`: useful when number of items requested needs to be factored into total complexity
* :ref:`overriding Object cost <overriding_object_cost>`: useful when the complexity of requesting multiple objects diminishes as the number of items requested increases

Cost analysis works with simple queries, queries with fragments, and mutations.

.. _complexity_multiplier:

Complexity Multiplier - Why and How?
------------------------------------

Complexity multiplier allows you to multiply the complexity of Object/Type by the quantity requested.

Why?
^^^^

For a query that resolves to a list of objects.
You probably want to factor the number of items requested into the query complexity.

For instance, you have a `posts` query that returns a list of `Post` objects.

.. code-block:: graphql

    type Post @cost(complexity: 5) {
        postId: ID!
        title: String
    }

    type Query {
        posts(first: Int): [Post]   // The complexity should be `first * 5`
    }

The complexity should be the value of `first` multiplied by `5`.

How?
^^^^

All you need to do is to add the `@cost` directive to your `Query` and specify the multipliers as a list of string

.. code-block:: graphql

    type Post @cost(complexity: 5) {
        postId: ID!
        title: String
    }

    type Query {
        posts(first: Int): [Post]   @cost(multiplier: ["first"])
    }


With the schema above, the complexity of the query below will be `4 * 5 = 20`.

.. code-block:: graphql

    {
        posts(first: 4) {
            postId
            title
        }
    }

What If There Is Field-specific Cost?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your Object type imposed extra complexities for specific fields as such:

.. code-block:: graphql

    type Post @cost(complexity: 5) {
        postId: ID!
        title: String   @cost(complexity: 4)
    }

    type Query {
        posts(first: Int): [Post]   @cost(multiplier: ["first"])
    }

and with such query:

.. code-block:: graphql

    {
        posts(first: 4) {
            postId
            title
        }
    }

The complexity will be `4 * (5 + 4) = 36`.


.. _overriding_object_cost:

Overriding Cost of Object Type
-------------------------------

You can also override the complexity of Object type defined.
All you need is to add the `complexity` argument
into the `@cost` directive to the Query type that returns the Object you're overriding.

.. code-block:: graphql

    type Post @cost(complexity: 5) {
        postId: ID!
        title: String   @cost(complexity: 4)
    }

    type Query {
        posts(first: Int!): [Post]   @cost(multiplier: ["first"], complexity: 2)
        post(postId: ID!): Post     // The complexity remains unchanged
    }

The cost of Post (`5`) will be overridden with `2` when querying `posts(first: Int!): [Post]`.

For instance, the total complexity will be `4 * (2 + 4) = 24`

.. code-block:: graphql

    {
        posts(first: 4) {
            postId
            title
        }
    }
