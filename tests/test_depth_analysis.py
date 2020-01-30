from graphql import execute, parse

from graphql_utils.execution import ExtendedExecutionContext
from tests.helpers import assert_no_errors, assert_has_errors, assert_has_exactly_n_errors, assert_has_error_message
from tests.schema import schema


def describe_depth_analysis():
    def _execute_query(max_depth: int):
        query = '{ field_1_str field_2_int field_3_obj { field_3_obj_sub_1 { xxx } } }'
        return execute(schema=schema, document=parse(query),
                       context_value={"depth_analysis": {
                           "max_depth": max_depth
                       }},
                       execution_context_class=ExtendedExecutionContext)

    def test_query_less_than_max_depth_allowed():
        result = _execute_query(10)
        assert_no_errors(result)

    def test_query_exceeding_max_depth():
        result = _execute_query(2)
        assert_has_errors(result)
        assert_has_exactly_n_errors(result, n=1)
        assert_has_error_message(result, error_message="Reached max depth of 2")
