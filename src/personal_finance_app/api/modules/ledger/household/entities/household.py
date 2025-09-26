from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from personal_finance_app.api.modules.ledger.household.entities.errors import HouseholdErrors
from personal_finance_app.api.modules.ledger.household.entities.member import Member
from personal_finance_app.api.sharedkernel.domain.base_entity import BaseEntity
from personal_finance_app.api.sharedkernel.domain.error import Error
from personal_finance_app.api.sharedkernel.domain.result import Result


@dataclass()
class Household(BaseEntity):
    name: str
    description: str
    members: List[Member] = field(default_factory=list)

    def __init__(self, name: str, description: str):

        super().__init__()
        self.name = name
        self.description = description
        self.members = []

    @classmethod
    def create(cls, name: str, description: str) -> Result[Household]:
        errors: List[Error] = []

        for validate in (
            lambda: cls._validate_name(name),
            lambda: cls._validate_description(description),
        ):
            errors.extend(validate())

        if len(errors) > 0:
            return Result.failure(errors)

        household = Household(name, description)
        return Result.success(household)

    @staticmethod
    def _validate_name(name: str) -> List[Error]:

        if not name or name.isspace():
            return [HouseholdErrors.invalid_name()]

        return []

    @staticmethod
    def _validate_description(description: str) -> List[Error]:

        if not description or description.isspace():
            return [HouseholdErrors.invalid_description()]

        return []

    def add_member(self, member: Member) -> Result[None]:

        if any(
            existing_member.email.lower() == member.email.lower()
            for existing_member in self.members
        ):
            return Result.failure(
                [HouseholdErrors.member_already_added_to_household(member.email)]
            )

        self.members.append(member)
        return Result.success(None)

    def remove_member(self, member: Member) -> Result[None]:

        if not any(
            existing_member.email.lower() == member.email.lower()
            for existing_member in self.members
        ):
            return Result.failure(
                [
                    HouseholdErrors.member_does_not_exist_in_household(
                        member.email.lower()
                    )
                ]
            )

        for counter, existing_member in enumerate(self.members):
            if existing_member.email.lower() == member.email.lower():
                del self.members[counter]
                return Result.success(None)
