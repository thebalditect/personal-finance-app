import pytest
from personal_finance_app.api.modules.ledger.householdaggregate.user import User


def test_new_should_create_user_instance():
    name = "Mandar Dharmadhikari"
    email = "test@value.com"
    user = User(name, email)

    assert user.name == name
    assert user.email == email
    assert user.id is not None


def test_invalid_name_should_raise_value_error():

    email = "mandar@test.com"

    with pytest.raises(ValueError, match="name cannot be empty or whitespace."):
        User("", email)
    with pytest.raises(ValueError, match="name cannot be empty or whitespace."):
        User(" ", email)


def test_invalid_email_should_raise_value_error():

    name = "Mandar Dharmadhikari"

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        User(name, "")

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        User(name, " ")

    with pytest.raises(ValueError, match="email should be of format abc@example.com."):
        User(name, "abc")
