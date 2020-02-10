"""
Directives

Sample source code:
    GraphQLIncludeDirective = GraphQLDirective(
        name="include",
        locations=[
            DirectiveLocation.FIELD,
            DirectiveLocation.FRAGMENT_SPREAD,
            DirectiveLocation.INLINE_FRAGMENT,
        ],
        args={
            "if": GraphQLArgument(
                GraphQLNonNull(GraphQLBoolean), description="Included when true."
            )
        },
        description="Directs the executor to include this field or fragment"
        " only when the `if` argument is true.",
    )

    How to use?
        skip = get_directive_values(GraphQLSkipDirective, node, self.variable_values)

Ref:
- https://github.com/graphql-python/graphql-core-next/issues/65
- http://spec.graphql.org/June2018/#sec-Type-System.Directives
"""
from graphql import build_schema

cost_directive_source_doc = """
    directive @cost(
        complexity: Int
        multipliers: [String]
    ) on FIELD_DEFINITION | OBJECT
"""

schema_with_cost_directive = build_schema(source=cost_directive_source_doc, no_location=True)

GraphQLCostDirective = schema_with_cost_directive.get_directive("cost")
