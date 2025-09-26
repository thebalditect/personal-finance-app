
from unittest.mock import Mock
from personal_finance_app.api.modules.ledger.household.application.repositories.household import HouseholdRepository
from personal_finance_app.api.modules.ledger.household.entities.errors import HouseholdErrors
from personal_finance_app.api.modules.ledger.household.features.create_household.command import CreateHouseholdCommand
from personal_finance_app.api.modules.ledger.household.features.create_household.handler import CreateHouseholdCommandHandler
from personal_finance_app.api.sharedkernel.domain.result import Result



def test_handle_shoud_return_success_result_for_valid_command():

    repository : HouseholdRepository = Mock()
    repository.save.return_value = Result.success(None)

    command = CreateHouseholdCommand(name= "The Balditect Household", description= "The household of the balditect.")

    handler = CreateHouseholdCommandHandler(repository= repository)

    result = handler.handle(command= command)

    assert result.is_success
    assert not result.is_failure

def test_handle_should_return_failure_result_for_invalid_household(invalid_household_data):
    
    respository: HouseholdRepository = Mock()
    respository.save.return_Value = Result.success(None)

    command = CreateHouseholdCommand(name= invalid_household_data.name, description= invalid_household_data.description)
    
    handler = CreateHouseholdCommandHandler(repository= respository)

    result = handler.handle(command= command)

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 2
    expected_errors = [HouseholdErrors.invalid_name(), HouseholdErrors.invalid_description()]
    assert result.errors == expected_errors