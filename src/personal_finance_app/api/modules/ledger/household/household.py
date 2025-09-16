from dataclasses import dataclass, field
from typing import List
from personal_finance_app.api.modules.ledger.household.member import Member
from personal_finance_app.api.sharedkernel.domain.base_entity import BaseEntity


@dataclass()
class Household(BaseEntity):
    name: str
    description: str
    members: List[Member] = field(default_factory=list)

    def __init__(self, name: str, description: str):

        if not name or name.isspace():
            raise ValueError("Household name cannot be empty or whitespace string.")

        if not description or description.isspace():
            raise ValueError(
                "Household description cannot be empty or whitespace string."
            )

        super().__init__()

        self.name = name
        self.description = description
        self.members = []

    def add_member(self, member: Member):

        if any(
            existing_member.email.lower() == member.email.lower()
            for existing_member in self.members
        ):
            raise ValueError(
                f"Member {member.email} is already a member of the household."
            )

        self.members.append(member)

    def remove_member(self, member: Member):

        for counter, existing_member in enumerate(self.members):
            if existing_member.email.lower() == member.email.lower():
                del self.members[counter]
                break
