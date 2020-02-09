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
        self.operation_cost_calculator = {
            'QUERY': self.compute_query_cost,
            'MUTATION': self.compute_mutation_cost,
            'SUBSCRIPTION': self.compute_subscription_cost
        }

    def enter_operation_definition(self, node, key, parent, path, *args):
        """
        Ref: https://github.com/pa-bru/graphql-cost-analysis/blob/b0f41119955654b52f8943ceaf4eb35dfb68db4e/src/costAnalysis.js#L95
        """
        self.complexity += self.get_cost_compute_fn(operation_type=node.operation.name)()

        breakpoint()
        return IDLE

    def exit_operation_definition(self):
        """
        Ref: https://github.com/pa-bru/graphql-cost-analysis/blob/b0f41119955654b52f8943ceaf4eb35dfb68db4e/src/costAnalysis.js#L124
        """
        if self.cost > self.max_complexity:
            return self.context.report_error(
                GraphQLError(f"{self.complexity} exceeded max complexity of {self.max_complexity}"))

    def get_cost_compute_fn(self, operation_type):
        try:
            return self.operation_cost_calculator[operation_type]
        except KeyError:
            self.context.report_error(GraphQLError(f"Query cost could not be calculated for operation of type {operation_type}"))

    def compute_query_cost(self):
        pass

    def compute_mutation_cost(self):
        pass

    def compute_subscription_cost(self):
        pass