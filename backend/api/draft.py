from fastapi import APIRouter, HTTPException
from backend.models.schema import ChampSelect
from backend.service.draft_service import drafter

router = APIRouter(tags=["draft"])


@router.post("/send")
def send_draft(data: ChampSelect):
    res = drafter(data.enemy, data.allies)

    return res