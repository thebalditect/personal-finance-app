from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime, timezone


@dataclass
class BaseEntity:
    id: UUID = field(default_factory=uuid4, init=False)
    created_on: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc), init=False
    )

    def __eq__(self, other):

        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
