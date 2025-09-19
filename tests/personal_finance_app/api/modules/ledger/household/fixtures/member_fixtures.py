from dataclasses import dataclass
from datetime import datetime
import pytest

from personal_finance_app.api.modules.ledger.household.member_role import MemberRole


@dataclass
class MemberData:
    name: str
    email: str
    birth_date: datetime
    gender: str
    avatar: bytes
    role: MemberRole


@pytest.fixture
def valid_member_data():

    return MemberData(
        name="John Doe",
        email="john.doe@test.com",
        birth_date=datetime(1980, 1, 1),
        gender="Male",
        avatar=b"\x89PNG\r\n\x1a\n" + b"somebytes",
        role=MemberRole.ADMINISTRATOR,
    )


@pytest.fixture
def invalid_member_name():
    return ["", " "]


@pytest.fixture
def invalid_member_email():
    return ["", " ", "invalid email", "invalid@1", ".com"]


@pytest.fixture
def invalid_member_gender():
    return ["", " "]


@pytest.fixture
def invalid_member_avatar():
    return [b"", b" "]
