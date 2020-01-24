from graphql import Visitor, GraphQLError, BREAK, IDLE, ValidationContext
from graphql.language import ast


class DepthAnalysisVisitor(Visitor):
    def __init__(self, context: ValidationContext, max_depth: int = 10):
        self.max_depth = max_depth
        self.context = context

    def enter(self, node, key, parent, path, *args):
        if isinstance(node, ast.NameNode):
            depth = path.count("selection_set")
            if depth > self.max_depth:
                self.context.report_error(GraphQLError(f"Reached max depth of {self.max_depth}"))
                return BREAK

        return IDLE
