from graphql import Visitor, GraphQLError, BREAK, IDLE, ValidationContext
from graphql.language import ast


class DepthAnalysisVisitor(Visitor):
    def __init__(self, context: ValidationContext, max_depth: int = 10):
        self.max_depth = max_depth
        self.context = context

    def enter_name(self, node, key, parent, path, *args):
        if isinstance(node, ast.NameNode):
            depth = path.count("selection_set")
            if depth > self.max_depth:
                self.context.report_error(GraphQLError(f"Reached max depth of {self.max_depth}"))
                return BREAK

        return IDLE


class CostAnalysisVisitor(Visitor):
    def __init__(self, context: ValidationContext, max_complexity):
        self.context = context
        self.max_complexity = max_complexity
        self.complexity = 0  # Keep track of complexity so far

    def enter_operation_definition(self, node, key, parent, path, *args):
        """
        TODO

        1. get current field from schema or type info
        2. let field_type be the result of get_named_type(field.type)
        3. get_argument_values(field, child_node)
        4. get_directives of field_type
        5. get_arguments_from_directive
        6. ...

        Ref: https://github.com/pa-bru/graphql-cost-analysis/blob/b0f41119955654b52f8943ceaf4eb35dfb68db4e/src/costAnalysis.js#L95
        """
        cost_compute_fn = self.get_cost_compute_fn(operation_type=node.operation.name)
        if not cost_compute_fn:
            return BREAK

        self.complexity += cost_compute_fn()

        return IDLE

    def exit_operation_definition(self):
        """
        Ref: https://github.com/pa-bru/graphql-cost-analysis/blob/b0f41119955654b52f8943ceaf4eb35dfb68db4e/src/costAnalysis.js#L124
        """
        if self.complexity > self.max_complexity:
            return self.context.report_error(
                GraphQLError(f"{self.complexity} exceeded max complexity of {self.max_complexity}"))

    def get_cost_compute_fn(self, operation_type):
        fn = getattr(self, f"compute_{operation_type.lower()}_cost")

        if not fn:
            self.context.report_error(
                GraphQLError(f"Query cost could not be calculated for operation of type {operation_type}"))

        return fn

    def compute_query_cost(self):
        pass

    def compute_mutation_cost(self):
        pass

    def compute_subscription_cost(self):
        pass
