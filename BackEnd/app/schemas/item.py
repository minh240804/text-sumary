from pydantic import BaseModel


class ItemResponse(BaseModel):
    item_id: int
    query_string: str | None = None
