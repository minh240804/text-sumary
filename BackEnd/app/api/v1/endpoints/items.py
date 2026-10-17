from fastapi import APIRouter

from app.schemas.item import ItemResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, q: str | None = None) -> ItemResponse:
    return ItemResponse(item_id=item_id, query_string=q)
