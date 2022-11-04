from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session

from app.crud import crud_guides
from app.db import get_db
from app.schemas.requests import GuideAddIn, GuideEditIn
from app.schemas.responses import GuideResponse, ItemResponse, StandardResponse
from app.service.bearer_auth import has_token

guide_router = APIRouter()


@guide_router.get("/", response_model=Page[GuideResponse])  #
def item_get_all(
    *,
    db: Session = Depends(get_db),
    params: Params = Depends(),
    search: str = None,
    sortOrder: str = "asc",
    sortColumn: str = "name",
    auth=Depends(has_token)
):

    sortTable = {"name": "name"}

    db_guides = crud_guides.get_guides(db, search, sortTable[sortColumn], sortOrder)
    return paginate(db_guides, params)


@guide_router.get("/{guide_uuid}", response_model=GuideResponse)  # , response_model=Page[UserIndexResponse]
def item_get_one(*, db: Session = Depends(get_db), guide_uuid: UUID, auth=Depends(has_token)):
    db_guide = crud_guides.get_guide_by_uuid(db, guide_uuid)

    return db_guide


@guide_router.post("/", response_model=GuideResponse)
def item_add(*, db: Session = Depends(get_db), guide: GuideAddIn, auth=Depends(has_token)):

    item_data = {
        "uuid": str(uuid4()),
        "name": guide.name,
        "text": guide.text,
        "text_jsonb": guide.text_jsonb,
        "created_at": datetime.now(timezone.utc),
    }

    new_item = crud_guides.create_guide(db, item_data)

    return new_item


@guide_router.patch("/{guide_uuid}", response_model=GuideResponse)
def item_edit(*, db: Session = Depends(get_db), guide_uuid: UUID, guide: GuideEditIn, auth=Depends(has_token)):

    db_guide = crud_guides.get_guide_by_uuid(db, guide_uuid)
    if not db_guide:
        raise HTTPException(status_code=400, detail="Item not found!")

    item_data = guide.dict(exclude_unset=True)
    item_data["updated_at"] = datetime.now(timezone.utc)

    new_item = crud_guides.update_guide(db, db_guide, item_data)

    return new_item


@guide_router.delete("/{guide_uuid}", response_model=StandardResponse)
def item_delete(*, db: Session = Depends(get_db), guide_uuid: UUID, auth=Depends(has_token)):

    db_guide = crud_guides.get_guide_by_uuid(db, guide_uuid)

    if not db_guide:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_guide)
    db.commit()

    return {"ok": True}
