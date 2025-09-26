from abc import ABC, abstractmethod
from uuid import uuid4

from personal_finance_app.api.modules.ledger.household.entities.household import Household
from personal_finance_app.api.sharedkernel.domain.result import Result

class HouseholdRepository(ABC):
    
    @abstractmethod
    def save(self, household: Household) -> Result[None]:
        pass

    @abstractmethod
    def get(self) -> Result[Household]:
        pass