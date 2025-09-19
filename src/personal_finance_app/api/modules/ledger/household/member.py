from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List
from personal_finance_app.api.modules.ledger.household.member_role import MemberRole
from personal_finance_app.api.sharedkernel.domain.base_entity import BaseEntity
from personal_finance_app.api.sharedkernel.domain.error_type import ErrorType
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

        _validate_name(name)
        _validate_email(email)
        _validate_age(birth_date)
        _validate_gender(gender)
        _validate_avatar(avatar)

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

    @staticmethod
    def create(
        name: str,
        email: str,
        birth_date: datetime,
        gender: str,
        avatar: bytes,
        role: MemberRole | None,
    ) -> Result[Member]:

        errors: List[Error] = []

        if not name or name.isspace():
            error = Error(
                code="Ledger.Household.ValidationError",
                description="name cannot be empty or whitespace.",
                error_type=ErrorType.VALIDATION,
            )
            errors.append(error)

        EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(EMAIL_REGEX, email) is None:
            error = Error(
                code="Ledger.Household.ValidationError",
                description="email should be of format abc@example.com.",
                error_type=ErrorType.VALIDATION,
            )
            errors.append(error)

        if not gender or gender.isspace():
            error = Error(
                code="Ledger.Household.ValidationError",
                description="gender should not be empty or just whitespace.",
                error_type=ErrorType.VALIDATION,
            )
            errors.append(error)

        if (
            not avatar
            or len(avatar) == 0
            or not avatar.startswith(b"\x89PNG\r\n\x1a\n")
        ):
            error = Error(
                code="Ledger.Household.ValidationError",
                description="avatar should be a valid png.",
                error_type=ErrorType.VALIDATION,
            )
            errors.append(error)

        if birth_date.date() == datetime.now().date():

            error = Error(
                code="Ledger.Household.ValidationError",
                description="birth date can not be today.",
                error_type=ErrorType.VALIDATION,
            )
            errors.append(error)

        if birth_date > datetime.now():
            error = Error(
                code="Ledger.Household.ValidationError",
                description="birth date cannot be in future.",
                error_type=ErrorType.VALIDATION,
            )
            errors.append(error)

        AGE_THRESHOLD: int = 16

        if (
            _calculate_age(birth_date) < AGE_THRESHOLD
            and birth_date <= datetime.now()
            and birth_date.date() != datetime.now().date()
        ):

            error = Error(
                code="Ledger.Household.ValidationError",
                description="member should be at least sixteen years old as on today.",
                error_type=ErrorType.VALIDATION,
            )
            errors.append(error)

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


def _calculate_age(birth_date: datetime) -> int:

    reference_date = datetime.today()

    age = reference_date.year - birth_date.year

    # Adjust if birthday hasn't occurred this year yet
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def _validate_age(birth_date: datetime):

    if birth_date > datetime.now():
        raise ValueError("birth date cannot be in future.")

    if birth_date.date() == datetime.now().date():
        raise ValueError("birth date can not be today.")

    AGE_THRESHOLD: int = 16

    if _calculate_age(birth_date) < AGE_THRESHOLD:
        raise ValueError("user should be at least sixteen years old as on today.")


def _validate_email(email: str):

    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.fullmatch(EMAIL_REGEX, email) is None:
        raise ValueError("email should be of format abc@example.com.")


def _validate_name(name: str):

    if not name or name.isspace():
        raise ValueError("name cannot be empty or whitespace.")


def _validate_gender(gender: str):

    if not gender or gender.isspace():
        raise ValueError("gender should not be empty or just whitespace.")


def _validate_avatar(avatar: bytes):

    if not avatar or len(avatar) == 0:
        raise ValueError("avatar cannot be empty.")

    if not avatar.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("avatar should be a valid png.")
