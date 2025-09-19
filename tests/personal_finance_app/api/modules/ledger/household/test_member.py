import pytest
from personal_finance_app.api.modules.ledger.household.member import Member
from datetime import datetime, timedelta

from personal_finance_app.api.modules.ledger.household.member_role import MemberRole


def test_new_should_create_user_instance(valid_member_data):
    user = Member(
        valid_member_data.name,
        valid_member_data.email,
        valid_member_data.birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
    )

    assert user.name == valid_member_data.name
    assert user.email == valid_member_data.email
    assert user.birth_date == valid_member_data.birth_date
    assert user.gender == valid_member_data.gender
    assert user.avatar == valid_member_data.avatar
    assert user.role == valid_member_data.role
    assert user.id is not None


def test_invalid_name_should_raise_value_error():

    email = "mandar@test.com"
    birth_date = datetime(1989, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(ValueError, match="name cannot be empty or whitespace."):
        Member("", email, birth_date, gender, avatar, role)
    with pytest.raises(ValueError, match="name cannot be empty or whitespace."):
        Member(" ", email, birth_date, gender, avatar, role)


def test_invalid_email_should_raise_value_error():

    name = "Mandar Dharmadhikari"
    birth_date = datetime(1989, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        Member(name, "", birth_date, gender, avatar, role)

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        Member(name, " ", birth_date, gender, avatar, role)

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        Member(name, "abc", birth_date, gender, avatar, role)


def test_user_should_not_be_born_in_future():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(2100, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(ValueError, match="birth date cannot be in future."):
        Member(name, email, birth_date, gender, avatar, role)


def test_user_should_not_be_born_today():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime.now()
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(ValueError, match="birth date can not be today."):
        Member(name, email, birth_date, gender, avatar, role)


def test_user_should_be_atleast_sixteen_years_old():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime.now() - timedelta(days=365)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(
        ValueError, match="user should be at least sixteen years old as on today."
    ):
        Member(name, email, birth_date, gender, avatar, role)


def test_gender_should_be_specified():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1989, 2, 12)
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(
        ValueError, match="gender should not be empty or just whitespace."
    ):
        Member(name, email, birth_date, "", avatar, role)

    with pytest.raises(
        ValueError, match="gender should not be empty or just whitespace."
    ):
        Member(name, email, birth_date, " ", avatar, role)


def test_avatar_should_not_be_of_empty():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1989, 2, 12)
    gender = "Male"
    avatar = b""
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(ValueError, match="avatar cannot be empty."):
        Member(name, email, birth_date, gender, avatar, role)


def test_avatar_should_not_be_of_other_than_png():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1989, 2, 12)
    gender = "Male"
    avatar = b"invalidbytes"
    role = MemberRole.ADMINISTRATOR

    with pytest.raises(ValueError, match="avatar should be a valid png."):
        Member(name, email, birth_date, gender, avatar, role)


def test_default_role_assigned_should_be_regular_if_not_specified():

    name = "Mandar Dharmadhikari"
    email = "test@value.com"
    birth_date = datetime(1989, 1, 1)
    gender = "Male"
    avatar = b"\x89PNG\r\n\x1a\n" + b"somebytes"

    member = Member(name, email, birth_date, gender, avatar, None)

    assert member.role == MemberRole.REGULAR
