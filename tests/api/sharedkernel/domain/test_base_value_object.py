import pytest
from dataclasses import dataclass, field, FrozenInstanceError
from personal_finance_app.api.sharedkernel.domain.base_value_object import (
    BaseValueObject,
)


@dataclass(frozen=True)
class Money(BaseValueObject):
    amount: float = field(init=True)
    currency: str = field(init=True)


def test_value_object_should_be_identical_based_on_value():
    money1 = Money(100, "INR")
    money2 = Money(100, "INR")

    assert money1 == money2


def test_value_object_should_be_immutable():
    money1 = Money(100, "INR")

    with pytest.raises(FrozenInstanceError):
        money1.amount = 200


def test_value_object_should_equate_all_properties():
    money1 = Money(100, "INR")
    money2 = Money(100, "USD")
    money3 = Money(200, "USD")

    assert money1 != money2
    assert money2 != money3
    assert money1 != money3
