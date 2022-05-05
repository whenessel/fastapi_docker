from datetime import datetime, time, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlmodel import Session, select

from app.config import get_settings
from app.db import get_session
from app.models.models import Accounts, Files, Ideas, StandardResponse
from app.service.bearer_auth import has_token

stats_router = APIRouter()


@stats_router.get("/", name="stats:List")
async def ideas_get_all(*, session: Session = Depends(get_session), auth=Depends(has_token)):

    return {"stats": "ok"}
