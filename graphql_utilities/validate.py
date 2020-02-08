from typing import List, Any

from graphql import GraphQLError, GraphQLSchema, DocumentNode, ValidationContext, visit

from graphql_utilities.visitor import DepthAnalysisVisitor


class ValidationAbortedError(RuntimeError):
    """
    Taken from: graphql-core-next/graphql.validation.validate
    Error when a validation has been aborted (error limit reached).
    """
    pass


def validate_depth(
        schema: GraphQLSchema,
        document: DocumentNode,
        context_value: Any = None,
) -> List[GraphQLError]:
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

    return errors
