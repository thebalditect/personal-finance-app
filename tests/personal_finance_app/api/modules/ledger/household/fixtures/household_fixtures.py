from dataclasses import dataclass
import pytest


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
