from pydantic import BaseModel

class CreateHouseholdCommand(BaseModel):
    name: str
    description: str