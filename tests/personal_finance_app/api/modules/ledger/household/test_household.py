import pytest
from datetime import datetime
from personal_finance_app.api.modules.ledger.household.errors import HouseholdErrors
from personal_finance_app.api.modules.ledger.household.household import (
    Household,
)
from personal_finance_app.api.modules.ledger.household.member import Member
from personal_finance_app.api.modules.ledger.household.member_role import MemberRole


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


def test_new_should_return_correct_household_instance():

    household_name = "The Balditect House"
    household_description = "The household of the balditect"

    household = Household(household_name, household_description)

    assert household.name == household_name
    assert household.description == household_description
    assert household.id is not None


def test_add_member_should_add_member_to_household():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1986, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    member = Member(name, email, birth_date, gender, avatar, role)

    hosehold_name = "The Balditect Household."
    household_decription = "This is the description of the balditect household."

    household = Household(hosehold_name, household_decription)

    household.add_member(member)

    assert len(household.members) == 1
    assert household.members[0] == member
    assert household.members[0].email == email


def test_same_user_cannot_be_added_again_to_the_household():

    hosehold_name = "The Balditect Household."
    household_decription = "This is the description of the balditect household."

    household = Household(hosehold_name, household_decription)

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1986, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    member = Member(name, email, birth_date, gender, avatar, role)

    household.add_member(member)

    with pytest.raises(
        ValueError, match=f"Member {member.email} is already a member of the household."
    ):
        household.add_member(member)


def test_remove_user_should_remove_user_from_the_household():

    hosehold_name = "The Balditect Household."
    household_decription = "This is the description of the balditect household."

    household = Household(hosehold_name, household_decription)

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1986, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    member1 = Member(name, email, birth_date, gender, avatar, role)

    email2 = "test@test.com"
    role2 = MemberRole.REGULAR
    member2 = Member(name, email2, birth_date, gender, avatar, role2)

    household.add_member(member1)
    household.add_member(member2)

    household.remove_member(member1)

    assert len(household.members) == 1
    assert household.members[0].id == member2.id
    assert household.members[0].email.lower() == member2.email.lower()
