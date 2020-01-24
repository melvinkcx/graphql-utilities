from typing import Any, Dict, Union, List, Optional

from graphql import GraphQLError, ExecutionContext, GraphQLSchema, DocumentNode, \
    GraphQLFieldResolver, GraphQLTypeResolver, Middleware, ValidationContext, TypeInfo, visit

from graphql_utils.visitor import DepthAnalysisVisitor

ContextValue = Optional[Dict[str, Any]]


class ValidationAbortedError(RuntimeError):
    """
    Taken from: graphql-core-next/graphql.validation.validate
    Error when a validation has been aborted (error limit reached).
    """
    pass


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
        errors: List[GraphQLError] = []

        def on_error(error: GraphQLError) -> None:
            errors.append(error)
            raise ValidationAbortedError

        depth_analysis = context_value.get("depth_analysis")
        if depth_analysis:
            max_depth = depth_analysis.get("max_depth", 10)
            context = ValidationContext(schema=schema, ast=document, type_info=TypeInfo(schema), on_error=on_error)

            try:
                visit(document, DepthAnalysisVisitor(context=context, max_depth=max_depth))
            except ValidationAbortedError:
                pass

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
