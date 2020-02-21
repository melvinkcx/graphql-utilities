.. _introduction:

Introduction
============

**graphql-utilities** tries to secure your GraphQL API from malicious queries and provides utilities to make using `graphql-core` easier.

1. It comes with a configurable `ExtendedExecutionContext` class that is capable of performing:

   * **query cost analysis**: define the cost of your queries using the `@cost()` directive provided, `graphql-utilities` provides helper functions and extended execution context to protect you from overly complex or costly queries.
   * **depth limiting**: limit the maximum depth of queries, it's especially useful with object types with recursive relationship

2. It also ships decorators for:

   * **resource-level/one-shot middleware**: middleware in `graphql-core` is run at field-level, it is handly when you need your middleware to run only once, especially auth-related middleware.

Getting Started
===============

You can install graphql-utilities using `pip <https://pip.pypa.io/>`_:

.. code-block:: shell

    pip install graphql-utilities

Alternatively, if you are using `pipenv <https://pipenv.kennethreitz.org/en/latest/>`_:

.. code-block:: shell

    pipenv install graphql-utilities

Note that **graphql-utilities** requires *graphql-core>=3.0*, which also means you need Python 3.6 or above,

With the package installed, you are ready to go. Depending on your need, you may refer to each page:

* :ref:`query_cost_analysis`
* :ref:`depth_limiting`
* :ref:`oneshot_middleware`