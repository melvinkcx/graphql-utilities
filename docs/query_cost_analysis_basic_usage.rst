Step 2: Define Complexity Of Queries/Objects/Fields (Basic Usage)
------------------------------------------------------------------

To define the complexity of a query, simple add a `@cost()` directive to any **Object** or **Field Definition**.

Complexity of Object
^^^^^^^^^^^^^^^^^^^^

To define the complexity of an Object Type, add `@cost(complexity: <Int>)` directive after the type identifier (`post`, in the case below).

.. code-block:: graphql

    type Post @cost(complexity: 5) {
        postId: ID!
        title: String
    }

    type Query {
        post(postId: ID!): Post
    }

The complexity of each Post object is **5**. The complexity of querying the schema `post(postId: ID!)` is also **5**.


Complexity of Field
^^^^^^^^^^^^^^^^^^^

You can always define field-specific complexity by adding a `@cost()` directive to a field:

.. code-block:: graphql

    type Post {
        postId: ID!
        title: String
        lastSnapshot: String @cost(complexity: 8)
    }

    type Query {
        post(postId: ID!): Post
    }

The complexity of the query below will be **8**.

.. code-block:: graphql

    {
        posts(postId: "XXXXXX") {
            postId
            lastSnapshot
        }
    }

Defining Complexity For Both Object and Fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In situation when complexity needs to be defined in Object as well as specific Field of the Object, such as:

.. code-block:: graphql

    type Post @cost(complexity: 5) {
        postId: ID!
        title: String
        lastSnapshot: String @cost(complexity: 8)
    }

The total complexity of querying an Object with the field `lastSnapshot` will be the sum of complexities defined in both @cost() directives (`5 + 8 = 13`).

.. code-block:: graphql

    {
        posts(postId: "XXXXXX") {
            postId
            lastSnapshot
        }
    }

The cost of the query above is `5 + 8 = 13`.

