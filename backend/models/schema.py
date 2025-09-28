from pydantic import BaseModel

class ChampSelect(BaseModel):
    enemy: list[str]
    allies: list[str]

