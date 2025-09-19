import pytest
from personal_finance_app.api.modules.ledger.household.member import Member
from datetime import datetime, timedelta

from personal_finance_app.api.modules.ledger.household.member_role import MemberRole
from personal_finance_app.api.sharedkernel.domain.error import Error, ErrorType


def test_create_should_return_success_result(valid_member_data):

    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        valid_member_data.birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
    )

    assert result.is_success
    assert not result.is_failure

    member = result.value
    assert member.name == valid_member_data.name
    assert member.email == valid_member_data.email
    assert member.birth_date == valid_member_data.birth_date
    assert member.gender == valid_member_data.gender
    assert member.avatar == valid_member_data.avatar
    assert member.role == valid_member_data.role
    assert member.id is not None


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


def test_for_invalid_name_create_should_return_failure_result(
    valid_member_data, invalid_member_name
):

    for name in invalid_member_name:
        result = Member.create(
            name,
            valid_member_data.email,
            valid_member_data.birth_date,
            valid_member_data.gender,
            valid_member_data.avatar,
            valid_member_data.role,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        expected_error = Error(
            code="Ledger.Household.ValidationError",
            description="name cannot be empty or whitespace.",
            error_type=ErrorType.VALIDATION,
        )
        assert result.errors[0] == expected_error


def test_for_invalid_email_create_should_return_failure_result(
    valid_member_data, invalid_member_email
):

    for email in invalid_member_email:
        result = Member.create(
            valid_member_data.name,
            email,
            valid_member_data.birth_date,
            valid_member_data.gender,
            valid_member_data.avatar,
            valid_member_data.role,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        expected_error = Error(
            code="Ledger.Household.ValidationError",
            description="email should be of format abc@example.com.",
            error_type=ErrorType.VALIDATION,
        )
        assert result.errors[0] == expected_error


def test_for_invalid_gender_create_should_return_failure_result(
    valid_member_data, invalid_member_gender
):
    for gender in invalid_member_gender:
        result = Member.create(
            valid_member_data.name,
            valid_member_data.email,
            valid_member_data.birth_date,
            gender,
            valid_member_data.avatar,
            valid_member_data.role,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        expected_error = Error(
            code="Ledger.Household.ValidationError",
            description="gender should not be empty or just whitespace.",
            error_type=ErrorType.VALIDATION,
        )
        assert result.errors[0] == expected_error


def test_for_non_png_type_avatar_create_should_return_failure_result(
    valid_member_data, invalid_member_avatar
):
    for avatar in invalid_member_avatar:
        result = Member.create(
            valid_member_data.name,
            valid_member_data.email,
            valid_member_data.birth_date,
            valid_member_data.gender,
            avatar,
            valid_member_data.role,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        expected_error = Error(
            code="Ledger.Household.ValidationError",
            description="avatar should be a valid png.",
            error_type=ErrorType.VALIDATION,
        )
        assert result.errors[0] == expected_error


def test_if_not_specified_default_member_role_should_be_regular(valid_member_data):
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        valid_member_data.birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        None,
    )

    assert result.is_success
    assert not result.is_failure

    member = result.value
    assert member.name == valid_member_data.name
    assert member.email == valid_member_data.email
    assert member.birth_date == valid_member_data.birth_date
    assert member.gender == valid_member_data.gender
    assert member.avatar == valid_member_data.avatar
    assert member.role == MemberRole.REGULAR
    assert member.id is not None


def test_create_should_return_failure_result_while_creating_member_born_today(
    valid_member_data,
):

    birth_date = datetime.now()
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
    )

    assert result.is_failure
    assert not result.is_success

    expected_error = Error(
        code="Ledger.Household.ValidationError",
        description="birth date can not be today.",
        error_type=ErrorType.VALIDATION,
    )

    assert len(result.errors) == 1
    assert result.errors[0] == expected_error


def test_create_should_return_failure_result_while_creating_unborn_member(
    valid_member_data,
):

    birth_date = datetime(2100, 1, 1)
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
    )

    assert result.is_failure
    assert not result.is_success

    expected_error = Error(
        code="Ledger.Household.ValidationError",
        description="birth date cannot be in future.",
        error_type=ErrorType.VALIDATION,
    )

    assert len(result.errors) == 1
    assert result.errors[0] == expected_error


def test_create_should_return_failure_result_while_creating_member_younger_than_sixteen_years(
    valid_member_data,
):

    birth_date = datetime.now() - timedelta(days=39)
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
    )

    assert result.is_failure
    assert not result.is_success

    expected_error = Error(
        code="Ledger.Household.ValidationError",
        description="member should be at least sixteen years old as on today.",
        error_type=ErrorType.VALIDATION,
    )

    assert len(result.errors) == 1
    assert result.errors[0] == expected_error


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
