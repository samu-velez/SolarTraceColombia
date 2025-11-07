from typing import Optional
from fastapi import APIRouter, HTTPException
from ..services import aggregations as ag

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/production-by-source")
def production_by_source(country: Optional[str] = None, year: Optional[int] = None):
    try:
        y, items = ag.production_by_source(country, year)
        return {"year": y, "items": items}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/renewables-share")
def renewables_share(country: Optional[str] = None, year: Optional[int] = None):
    y, data = ag.renewables_share_breakdown(country, year)
    return {"year": y, **data}

@router.get("/installed-capacity-trends")
def capacity_trends(country: Optional[str] = None):
    return ag.installed_capacity_trends(country)

@router.get("/renewable-vs-conventional")
def ren_vs_conv(country: Optional[str] = None):
    return ag.renewable_vs_conventional(country)