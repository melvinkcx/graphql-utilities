from typing import List, Any

from graphql import GraphQLError, GraphQLSchema, DocumentNode, ValidationContext, visit, TypeInfo

from graphql_utilities.exceptions import ValidationAbortedError
from graphql_utilities.visitor import DepthAnalysisVisitor, CostAnalysisVisitor


def validate_depth(
        schema: GraphQLSchema,
        document: DocumentNode,
        context_value: Any,
        errors: List[GraphQLError]
):
    def on_error(error: GraphQLError) -> None:
        errors.append(error)
        raise ValidationAbortedError

    depth_analysis = context_value.get("depth_analysis")

    if depth_analysis:
        max_depth = depth_analysis.get("max_depth", 10)
        context = ValidationContext(schema=schema, ast=document, type_info=TypeInfo(schema), on_error=on_error)

        visit(document, DepthAnalysisVisitor(context=context, max_depth=max_depth))


def validate_cost(
        schema: GraphQLSchema,
        document: DocumentNode,
        context_value: Any,
        errors: List[GraphQLError]
):
    def on_error(error: GraphQLError) -> None:
        errors.append(error)
        raise ValidationAbortedError

    cost_analysis = context_value.get("cost_analysis")

    if cost_analysis:
        max_complexity = cost_analysis.get("max_complexity", 500)
        context = ValidationContext(schema=schema, ast=document, type_info=TypeInfo(schema), on_error=on_error)

        visit(document, CostAnalysisVisitor(context=context, max_complexity=max_complexity))

    return []
