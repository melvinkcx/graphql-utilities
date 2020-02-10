from functools import reduce
from typing import Tuple, List, Union

from graphql import Visitor, GraphQLError, BREAK, IDLE, ValidationContext, GraphQLInterfaceType, GraphQLObjectType, \
    GraphQLField, get_named_type
from graphql.execution.values import get_argument_values, get_directive_values
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
        self.operation_multipliers = []
        self.total_complexity = 0  # Keep track of complexity so far

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

        self.total_complexity += cost_compute_fn(node=node)

        return IDLE

    def exit_operation_definition(self):
        """
        Ref: https://github.com/pa-bru/graphql-cost-analysis/blob/b0f41119955654b52f8943ceaf4eb35dfb68db4e/src/costAnalysis.js#L124
        """
        if self.total_complexity > self.max_complexity:
            return self.context.report_error(
                GraphQLError(f"{self.total_complexity} exceeded max complexity of {self.max_complexity}"))

    def get_cost_compute_fn(self, operation_type):
        fn = getattr(self, f"compute_{operation_type.lower()}_cost")

        if not fn:
            self.context.report_error(
                GraphQLError(f"Query cost could not be calculated for operation of type {operation_type}"))

        return fn

    def compute_query_cost(self, node):
        return self.compute_node_cost(
            node=node,
            type_definition=self.context.schema.query_type
        )

    def compute_mutation_cost(self, node):
        # TODO
        pass

    def compute_subscription_cost(self, node):
        # TODO
        pass

    def compute_node_cost(self, node, type_definition, parent_multiplier=None):
        if not parent_multiplier:
            parent_multiplier = []

        if not node.selection_set:
            return 0

        fields = {}
        if isinstance(type_definition, GraphQLObjectType) or isinstance(type_definition, GraphQLInterfaceType):
            fields = type_definition.fields

        total_cost = 0
        fragment_cost = []  # TODO ??
        variables = {}  # TODO get variables from operation
        selections = node.selection_set.selections
        for selection in selections:
            self.operation_multipliers = [*parent_multiplier]
            node_cost = 0

            if selection.kind == 'field':
                # Calculate cost for FieldNode
                field: GraphQLField = fields[selection.name.value]
                if not field:
                    break

                field_type = get_named_type(field.type)
                field_args = get_argument_values(field, selection, variables)

                cost_is_computed = False
                if field.ast_node and \
                        field.ast_node.directives:
                    directive_args: Union[Tuple[int, List], None] = self.get_args_from_directives(
                        directives=field.ast_node.directives,
                        field_args=field_args
                    )
                    node_cost = self.compute_cost(directive_args)

                    if directive_args:
                        cost_is_computed = True

                if field_type and \
                        field_type.ast_node and \
                        field_type.ast_node.directives and \
                        isinstance(field_type, GraphQLObjectType) and \
                        not cost_is_computed:
                    directive_args = self.get_args_from_directives(directives=field_type.ast_node.directives,
                                                                   field_args=field_args)
                    node_cost = self.compute_cost(directive_args)

                child_cost = self.compute_node_cost(node=selection, type_definition=field_type,
                                                    parent_multiplier=self.operation_multipliers) or 0
                node_cost += child_cost

            elif selection.kind == 'fragment_spread':
                pass
            elif selection.kind == 'inline_fragment':
                pass
            else:
                node_cost = self.compute_node_cost(node=selection, type_definition=type_definition)

            total_cost += max(node_cost, 0)

        return total_cost

    def get_args_from_directives(self, directives, field_args) -> Union[None, Tuple[Union[int, None], List]]:
        cost_directive = None
        cost_directives = list(filter(lambda d: d.name.value == 'cost', directives))
        if len(cost_directives) > 0:
            cost_directive = cost_directives[0]

        if cost_directive and cost_directive.arguments:
            complexity_arg = None
            complexity_args = list(filter(lambda a: a.name.value == 'complexity', cost_directive.arguments))
            if len(complexity_args) > 0:
                complexity_arg = complexity_args[0]

            multipliers_arg = None
            multipliers_args = list(filter(lambda a: a.name.value == 'multipliers', cost_directive.arguments))
            if len(multipliers_args) > 0:
                multipliers_arg = multipliers_args[0]

            complexity = int(
                complexity_arg.value.value) if complexity_arg and complexity_arg.value and complexity_arg.value.kind == "int_value" else None
            multipliers = self.get_multipliers_from_list_node(multipliers_arg.value.values,
                                                              field_args) if multipliers_arg and multipliers_arg.value and multipliers_arg.value.kind == "list" else []

            return complexity, multipliers

    def compute_cost(self, directive_args: Tuple[int, List]) -> int:
        [complexity, multipliers] = directive_args

        use_multipliers = len(multipliers) > 0
        if use_multipliers:
            multiplier = reduce(
                lambda total, current: total + current,
                multipliers,
                0
            )
            self.operation_multipliers = [*self.operation_multipliers, multiplier]
            return reduce(
                lambda acc, mltp: acc * mltp,
                self.operation_multipliers,
                complexity
            )
        return complexity

    def get_multipliers_from_list_node(self, list_nodes, field_args):
        multipliers = list(map(lambda node: node.value, filter(lambda node: node.kind == "string", list_nodes)))
        return self.get_multipliers_from_string(multipliers, field_args)

    def get_multipliers_from_string(self, multipliers, field_args):
        # TODO
        pass
