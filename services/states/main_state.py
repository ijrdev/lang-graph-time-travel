from pydantic import BaseModel

class MainState(BaseModel):
    input: str
    subject_id: int
    query_builder: str | None = None
    searches: list | None = None
    topics: list | None = None
    content: str | None = None
