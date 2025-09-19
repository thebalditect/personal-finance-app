from personal_finance_app.api.sharedkernel.domain.error import Error
from personal_finance_app.api.sharedkernel.domain.error_type import ErrorType
from personal_finance_app.api.sharedkernel.domain.result import Result


class Dummy:
    name: str

    def __init__(self, name: str):
        self.name = name


def test_generic_success_result():

    dummy = Dummy("test")

    result = Result.success(dummy)

    assert result.is_success
    assert not result.is_failure
    assert result.value == dummy


def test_success_result_without_type():

    result = Result.success(None)

    assert result.is_success
    assert not result.is_failure
    assert result.value is None


def test_failure_result_with_single_error():

    error = Error("Error.Failure", "Failure error description.", ErrorType.FAILURE)

    result = Result.failure(error)

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors[0] == error


def test_failure_result_with_multiple_errors():

    error1 = Error(
        "Error.Validation", "Validation for field a failed", ErrorType.VALIDATION
    )
    error2 = Error(
        "Error.Validation", "Validation for field b failed", ErrorType.VALIDATION
    )

    result = Result.failure([error1, error2])

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 2
    assert result.errors[0] == error1
    assert result.errors[1] == error2
