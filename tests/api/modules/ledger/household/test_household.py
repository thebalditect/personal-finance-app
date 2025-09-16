import pytest
from datetime import datetime
from personal_finance_app.api.modules.ledger.household.household import (
    Household,
)
from personal_finance_app.api.modules.ledger.household.member import Member


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


def test_add_member_should_add_member_to_household():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1986, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"

    member = Member(name, email, birth_date, gender, avatar)

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

    member = Member(name, email, birth_date, gender, avatar)

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

    member1 = Member(name, email, birth_date, gender, avatar)

    email2 = "test@test.com"
    member2 = Member(name, email2, birth_date, gender, avatar)

    household.add_member(member1)
    household.add_member(member2)

    household.remove_member(member1)

    assert len(household.members) == 1
    assert household.members[0].id == member2.id
    assert household.members[0].email.lower() == member2.email.lower()
