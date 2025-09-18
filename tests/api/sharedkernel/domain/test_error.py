from personal_finance_app.api.sharedkernel.domain.error import Error, ErrorType


def test_error_with_failure_type():
    code = "Error.Failure"
    description = "This is sample error"

    error = Error.failure(code, description)

    assert error.code == code
    assert error.description == description
    assert error.error_type == ErrorType.FAILURE


def test_not_found_error():

    code = "Error.NotFound"
    description = "The item with id x was not found"
    error = Error.not_found(code, description)

    assert error.code == code
    assert error.description == description
    assert error.error_type == ErrorType.NOT_FOUND


def test_conflict_error():

    code = "Error.Conflict"
    description = "Item with id x already exists."
    error = Error.conflict(code, description)

    assert error.code == code
    assert error.description == description
    assert error.error_type == ErrorType.CONFLICT


def test_validation_error():

    code = "Error.Validation"
    description = "There are validation errors"
    error = Error.validation(code, description)

    assert error.code == code
    assert error.description == description
    assert error.error_type == ErrorType.VALIDATION
