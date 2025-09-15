from dataclasses import dataclass

from personal_finance_app.api.sharedkernel.domain.base_entity import BaseEntity


@dataclass()
class Household(BaseEntity):
    name: str
    description: str

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
