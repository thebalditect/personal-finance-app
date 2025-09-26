from dataclasses import dataclass

@dataclass(frozen= True)
class GetHouseholdQueryResponse():
    name: str
    description: str