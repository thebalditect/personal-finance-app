import re
from dataclasses import dataclass
from personal_finance_app.api.sharedkernel.domain.base_entity import BaseEntity


@dataclass
class User(BaseEntity):
    name: str
    email: str

    def __init__(self, name: str, email: str):

        if not name or name.isspace():
            raise ValueError("name cannot be empty or whitespace.")

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if re.fullmatch(email_regex, email) is None:
            raise ValueError("email should be of format abc@example.com.")

        super().__init__()
        self.name = name
        self.email = email
