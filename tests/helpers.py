from graphql import ExecutionResult


def assert_no_errors(result: ExecutionResult) -> None:
    assert not result.errors, "Results should contain errors"


def assert_no_data(result: ExecutionResult) -> None:
    assert not result.data, "Results shouldn't contain data"


def assert_has_data(result: ExecutionResult) -> None:
    assert result.data, "Results should contain data"


def assert_has_errors(result: ExecutionResult) -> None:
    assert result.errors, "ExecutionResult should contain errors"


def assert_has_exactly_n_errors(result: ExecutionResult, n: int) -> None:
    assert len(result.errors) == n, f"ExecutionResult should contain exactly {n} error(s)"


def assert_has_error_message(result: ExecutionResult, error_message: str) -> None:
    has_error_message = False
    for err in result.errors:
        if err.message.find(error_message) != -1:
            has_error_message = True

    assert has_error_message, f"'{error_message}' not found"
