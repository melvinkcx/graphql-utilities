from typing import List, Any

from graphql import execute, parse

from graphql_utils.decorators import run_only_once
from tests.helpers import assert_no_errors
from tests.schema import schema


def test_run_only_once():
    runs: List[Any] = []

    class Middleware:
        @run_only_once
        def resolve(self, next_, root, info, *args, **kwargs):
            runs.append(True)
            return next_(root, info, *args, **kwargs)

    query = '{ field_1_str field_2_int field_3_obj { field_3_obj_sub_1 { xxx } } }'

    result = execute(schema=schema, document=parse(query), middleware=[Middleware()])
    assert_no_errors(result)
    assert len(runs) == 1, "middleware should run only once"
