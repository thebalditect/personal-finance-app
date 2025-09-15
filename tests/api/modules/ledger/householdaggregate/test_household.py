import pytest
from personal_finance_app.api.modules.ledger.householdaggregate.household import (
    Household,
)


def test_new_should_return_correct_household_instance():

    household_name = "The Balditect House"
    household_description = "The household of the balditect"

    household = Household(household_name, household_description)

    assert household.name == household_name
    assert household.description == household_description
    assert household.id is not None


def test_invalid_name_should_raise_value_error():

    household_description = "The household for the balditect."

    with pytest.raises(
        ValueError, match="Household name cannot be empty or whitespace string."
    ):
        Household("", household_description)

    with pytest.raises(
        ValueError, match="Household name cannot be empty or whitespace string."
    ):
        Household(" ", household_description)

    with pytest.raises(
        ValueError, match="Household name cannot be empty or whitespace string."
    ):
        Household(None, household_description)


def test_invalid_description_should_raise_value_error():
    household_name = "The Balditect Household"

    with pytest.raises(
        ValueError, match="Household description cannot be empty or whitespace string."
    ):
        Household(household_name, "")

    with pytest.raises(
        ValueError, match="Household description cannot be empty or whitespace string."
    ):
        Household(household_name, " ")

    with pytest.raises(
        ValueError, match="Household description cannot be empty or whitespace string."
    ):
        Household(household_name, None)
