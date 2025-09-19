from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List
from personal_finance_app.api.modules.ledger.household.errors import HouseholdErrors
from personal_finance_app.api.modules.ledger.household.member_role import MemberRole
from personal_finance_app.api.sharedkernel.domain.base_entity import BaseEntity
from personal_finance_app.api.sharedkernel.domain.result import Result, Error


@dataclass
class Member(BaseEntity):
    name: str
    email: str
    birth_date: datetime
    gender: str
    avatar: bytes
    role: MemberRole | None

    def __init__(
        self,
        name: str,
        email: str,
        birth_date: datetime,
        gender: str,
        avatar: bytes,
        role: MemberRole | None,
    ):

        super().__init__()
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.gender = gender
        self.avatar = avatar

        if role is None:
            self.role = MemberRole.REGULAR
        else:
            self.role = role

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        birth_date: datetime,
        gender: str,
        avatar: bytes,
        role: MemberRole | None,
    ) -> Result[Member]:

        errors: List[Error] = []

        for validate in (
            lambda: cls._validate_name(name),
            lambda: cls._validate_email(email),
            lambda: cls._validate_age(birth_date),
            lambda: cls._validate_gender(gender),
            lambda: cls._validate_avatar(avatar),
        ):
            errors.extend(validate())

        if len(errors) > 0:
            return Result.failure(errors=errors)

        member = Member(
            name=name,
            email=email,
            birth_date=birth_date,
            gender=gender,
            avatar=avatar,
            role=role,
        )
        return Result.success(member)

    @staticmethod
    def _validate_name(name: str) -> List[Error]:
        if not name or name.isspace():
            return [HouseholdErrors.invalid_name()]

        return []

    @staticmethod
    def _validate_email(email: str) -> List[Error]:
        EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(EMAIL_REGEX, email) is None:
            return [HouseholdErrors.invalid_email()]

        return []

    @staticmethod
    def _validate_gender(gender: str) -> List[Error]:
        if not gender or gender.isspace():
            return [HouseholdErrors.invalid_gender()]

        return []

    @staticmethod
    def _validate_avatar(avatar: bytes) -> List[Error]:
        if (
            not avatar
            or len(avatar) == 0
            or not avatar.startswith(b"\x89PNG\r\n\x1a\n")
        ):
            return [HouseholdErrors.invalid_image_format()]

        return []

    @staticmethod
    def _validate_age(birth_date: datetime) -> List[Error]:
        if birth_date.date() > datetime.now().date():
            error = HouseholdErrors.unborn_member()
            return [error]

        AGE_THRESHOLD: int = 16

        reference_date = datetime.today()

        age = reference_date.year - birth_date.year

        # Adjust if birthday hasn't occurred this year yet
        if (reference_date.month, reference_date.day) < (
            birth_date.month,
            birth_date.day,
        ):
            age -= 1

        if age < AGE_THRESHOLD and birth_date.date() <= datetime.now().date():

            error = HouseholdErrors.member_younger_than_sixteen_years_of_age()
            return [error]

        return []

    @staticmethod
    def _calculate_age(birth_date: datetime) -> int:

        reference_date = datetime.today()

        age = reference_date.year - birth_date.year

        # Adjust if birthday hasn't occurred this year yet
        if (reference_date.month, reference_date.day) < (
            birth_date.month,
            birth_date.day,
        ):
            age -= 1

        return age
