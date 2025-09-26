from personal_finance_app.api.modules.ledger.household.application.repositories.household import HouseholdRepository
from personal_finance_app.api.modules.ledger.household.entities.household import Household
from personal_finance_app.api.modules.ledger.household.features.create_household.command import CreateHouseholdCommand
from personal_finance_app.api.sharedkernel.domain.result import Result


class CreateHouseholdCommandHandler():
    _repository: HouseholdRepository

    def __init__(self, repository: HouseholdRepository):
        self._repository = repository

    
    def handle(self, command: CreateHouseholdCommand) -> Result[None]:

        result = Household.create(name= command.name, description= command.description)
        if result.is_failure:
            return Result.failure(result.errors)
        
        self._repository.save(result.value)
        
        return Result.success(None)