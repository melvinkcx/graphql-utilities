from typing import Any, Dict, Union, List, Optional

from graphql import GraphQLError, ExecutionContext, GraphQLSchema, DocumentNode, \
    GraphQLFieldResolver, GraphQLTypeResolver, Middleware, ValidationContext, TypeInfo, visit

from graphql_utilities.validate import validate_depth

ContextValue = Optional[Dict[str, Any]]


class ExtendedExecutionContext(ExecutionContext):
    @classmethod
    def build(
            cls,
            schema: GraphQLSchema,
            document: DocumentNode,
            root_value: Any = None,
            context_value: Any = None,
            raw_variable_values: Dict[str, Any] = None,
            operation_name: str = None,
            field_resolver: GraphQLFieldResolver = None,
            type_resolver: GraphQLTypeResolver = None,
            middleware: Middleware = None,
    ) -> Union[List[GraphQLError], ExecutionContext]:
        # Build execution context after visiting it
        errors = validate_depth(schema=schema, document=document, context_value=context_value)

        if errors:
            return errors

        return super(ExtendedExecutionContext, cls).build(
            schema,
            document,
            root_value,
            context_value,
            raw_variable_values,
            operation_name,
            field_resolver,
            type_resolver,
            middleware
        )
