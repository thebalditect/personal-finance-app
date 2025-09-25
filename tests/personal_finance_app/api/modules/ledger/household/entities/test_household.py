from personal_finance_app.api.modules.ledger.household.entities.errors import HouseholdErrors
from personal_finance_app.api.modules.ledger.household.entities.household import (
    Household,
)


def test_create_should_return_success_result(valid_household_data):

    result = Household.create(
        name=valid_household_data.name, description=valid_household_data.description
    )
    assert result.is_success
    assert not result.is_failure
    assert result.value.name == valid_household_data.name
    assert result.value.description == valid_household_data.description


def test_create_should_return_failure_result_for_invalid_household_name(
    valid_household_data, invalid_household_name
):

    for name in invalid_household_name:
        result = Household.create(name, valid_household_data.description)

        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_name()


def test_create_should_return_failure_result_for_invalid_household_description(
    valid_household_data, invalid_household_description
):

    for description in invalid_household_description:
        result = Household.create(valid_household_data.name, description)

        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_description()


def test_create_should_return_all_validation_errors_with_failure_result(
    invalid_household_data,
):

    result = Household.create(
        invalid_household_data.name, invalid_household_data.description
    )

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 2

    expected_errors = [
        HouseholdErrors.invalid_name(),
        HouseholdErrors.invalid_description(),
    ]

    assert result.errors == expected_errors


def test_add_member_should_return_success_result(valid_household, valid_member):

    household = valid_household
    member = valid_member

    result = household.add_member(member)

    assert result.is_success
    assert not result.is_failure
    assert result.value is None


def test_add_member_should_return_failure_result_for_already_added_member(
    valid_household, valid_member
):

    household = valid_household
    member = valid_member

    household.add_member(member)
    result = household.add_member(member)

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors[0] == HouseholdErrors.member_already_added_to_household(
        member.email
    )


def test_remove_member_should_return_success_result(valid_household, valid_member):

    household = valid_household
    member = valid_member

    add_member_result = household.add_member(member)

    assert add_member_result.is_success
    assert len(household.members) == 1

    remove_member_result = household.remove_member(member)

    assert remove_member_result.is_success
    assert not remove_member_result.is_failure


def test_remove_user_should_return_failure_result_while_removing_non_existent_member(
    valid_household, valid_member
):

    household = valid_household
    member = valid_member

    result = household.remove_member(member)

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors[0] == HouseholdErrors.member_does_not_exist_in_household(
        member.email
    )
