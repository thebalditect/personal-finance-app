from dataclasses import dataclass
import pytest

from personal_finance_app.api.modules.ledger.household.entities.household import Household


@dataclass
class HouseholdData:
    name: str
    description: str


@pytest.fixture
def valid_household_data() -> HouseholdData:
    return HouseholdData(
        name="The Balditect Household",
        description="This is the house hold of the Balditect.",
    )


@pytest.fixture
def invalid_household_name():
    return ["", " "]


@pytest.fixture
def invalid_household_description():
    return ["", " "]


@pytest.fixture
def invalid_household_data():
    return HouseholdData(name="", description="")


@pytest.fixture
def valid_household(valid_household_data) -> Household:
    return Household.create(
        valid_household_data.name, valid_household_data.description
    ).value
