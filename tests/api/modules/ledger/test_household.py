from personal_finance_app.api.modules.ledger.householdaggregate.household import (
    Household,
)


def test_create_should_return_correct_household_instance():

    household_name = "The Balditect House"
    household_description = "The household of the balditect"

    household = Household(household_name, household_description)

    assert household.name == household_name
    assert household.description == household_description
    assert household.id is not None
