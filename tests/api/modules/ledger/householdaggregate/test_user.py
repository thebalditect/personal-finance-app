import pytest
from personal_finance_app.api.modules.ledger.householdaggregate.user import User
from datetime import datetime, timedelta


def test_new_should_create_user_instance():

    name = "Mandar Dharmadhikari"
    email = "test@value.com"
    birth_date = datetime(1989, 1, 1)
    gender = "Male"

    user = User(name, email, birth_date, gender)

    assert user.name == name
    assert user.email == email
    assert user.birth_date == birth_date
    assert user.gender == gender
    assert user.id is not None


def test_invalid_name_should_raise_value_error():

    email = "mandar@test.com"
    birth_date = datetime(1989, 1, 1)
    gender = "Male"

    with pytest.raises(ValueError, match="name cannot be empty or whitespace."):
        User("", email, birth_date, gender)
    with pytest.raises(ValueError, match="name cannot be empty or whitespace."):
        User(" ", email, birth_date, gender)


def test_invalid_email_should_raise_value_error():

    name = "Mandar Dharmadhikari"
    birth_date = datetime(1989, 1, 1)
    gender = "Male"

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        User(name, "", birth_date, gender)

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        User(name, " ", birth_date, gender)

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        User(name, "abc", birth_date, gender)


def test_user_should_not_be_born_in_future():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(2100, 1, 1)
    gender = "Male"

    with pytest.raises(ValueError, match="birth date cannot be in future."):
        User(name, email, birth_date, gender)


def test_user_should_not_be_born_today():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime.now()
    gender = "Male"

    with pytest.raises(ValueError, match="birth date can not be today."):
        User(name, email, birth_date, gender)


def test_user_should_be_atleast_sixteen_years_old():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime.now() - timedelta(days=365)
    gender = "Male"

    with pytest.raises(
        ValueError, match="user should be at least sixteen years old as on today."
    ):
        User(name, email, birth_date, gender)


def test_gender_should_be_specified():

    name = "Mandar Dharmadhikari"
    email = "mandar@test.com"
    birth_date = datetime(1989, 2, 12)

    with pytest.raises(
        ValueError, match="gender should not be empty or just whitespace."
    ):
        User(name, email, birth_date, "")

    with pytest.raises(
        ValueError, match="gender should not be empty or just whitespace."
    ):
        User(name, email, birth_date, " ")
