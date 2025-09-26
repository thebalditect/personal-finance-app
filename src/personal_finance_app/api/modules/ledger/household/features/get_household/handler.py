from personal_finance_app.api.modules.ledger.household.application.repositories.household import HouseholdRepository
from personal_finance_app.api.modules.ledger.household.features.get_household.response import GetHouseholdQueryResponse
from personal_finance_app.api.sharedkernel.domain.result import Result


class GetHouseholdQueryHandler():
    _respository: HouseholdRepository

    def __init__(self, repository: HouseholdRepository):
        self._respository = repository
    
    def handle(self) -> Result[GetHouseholdQueryResponse]:

        result = self._respository.get()

        if result.is_failure:
            return Result.failure(result.errors)
        
        query_response = GetHouseholdQueryResponse(name= result.value.name, description= result.value.description)
        return Result.success(query_response)
        
        