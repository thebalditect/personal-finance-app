
from unittest.mock import Mock
from personal_finance_app.api.modules.ledger.household.application.repositories.household import HouseholdRepository
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