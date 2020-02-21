from typing import Any, Dict, Union, List, Optional

from graphql import GraphQLError, ExecutionContext, GraphQLSchema, DocumentNode, \
    GraphQLFieldResolver, GraphQLTypeResolver, Middleware

from graphql_utilities.exceptions import ValidationAbortedError
from graphql_utilities.validate import validate_depth, validate_cost

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
        # As suggested, graphql_sync, graphql_impl, or graphql should be invoked to execute queries.
        # By invoking them, schema and documents will have already been validated before the execution
        # context is being created
        errors: List[GraphQLError] = []

        if context_value and isinstance(context_value, dict):
            try:
                validate_depth(schema=schema, document=document, context_value=context_value, errors=errors)
                validate_cost(schema=schema, document=document, context_value=context_value, errors=errors)
            except ValidationAbortedError:
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
