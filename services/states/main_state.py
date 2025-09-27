from pydantic import BaseModel

class MainState(BaseModel):
    input: str
    query_builder: str | None = None
    searches: list | None = None
    topics: list | None = None
