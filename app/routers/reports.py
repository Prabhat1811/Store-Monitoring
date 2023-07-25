from fastapi import APIRouter

router = APIRouter(tags=["reports"])


@router.post("/trigger_report")
async def trigger_report():
    pass


@router.get("/get_report")
async def get_report():
    pass
