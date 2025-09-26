
from unittest.mock import Mock
from personal_finance_app.api.modules.ledger.household.application.repositories.household import HouseholdRepository
from personal_finance_app.api.modules.ledger.household.entities.errors import HouseholdErrors
from personal_finance_app.api.modules.ledger.household.features.get_household.handler import GetHouseholdQueryHandler
from personal_finance_app.api.sharedkernel.domain.result import Result


def test_handler_should_return_success_reesult_when_household_exists(valid_household):

    repository: HouseholdRepository = Mock()
    repository.get.return_value = Result.success(valid_household)

    handler = GetHouseholdQueryHandler(repository = repository)

    result = handler.handle()

    assert result.is_success
    assert not result.is_failure
    assert result.value.name == valid_household.name
    assert result.value.description == valid_household.description

def test_handle_should_return_not_found_error_result_when_no_household_is_found():

    repository: HouseholdRepository = Mock()
    repository.get.return_value = Result.failure(HouseholdErrors.household_not_found())

    handler = GetHouseholdQueryHandler(repository= repository)

    result = handler.handle()

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors == [HouseholdErrors.household_not_found()]

def test_handle_should_return_multiple_househould_found_error_when_multiple_household_are_found():

    repository: HouseholdRepository = Mock()
    repository.get.return_value = Result.failure(HouseholdErrors.multiple_household_found())

    handler = GetHouseholdQueryHandler(repository= repository)

    result = handler.handle()

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors == [HouseholdErrors.multiple_household_found()]