from dataclasses import dataclass

from personal_finance_app.api.sharedkernel.domain.base_entity import BaseEntity


@dataclass()
class Household(BaseEntity):
    name: str
    description: str

    def __init__(self, name: str, description: str):
        super().__init__()

        self.name = name
        self.description = description
