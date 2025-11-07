from fastapi import APIRouter, HTTPException
from ..core.schemas import CalcRequest
from ..services import calculators as calc

router = APIRouter(prefix="/calc", tags=["calc"])

@router.post("/renewable-percentage")
def renewable_percentage(body: CalcRequest):
    try:
        return calc.user_renewable_percentage(body.kwh_total, body.country, body.year)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))