from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..core.schemas import UploadResponse, PaginatedRows
from ..services import dataset as ds

router = APIRouter(prefix="/dataset", tags=["dataset"])

@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        meta = ds.load_dataframe(content, file.filename)
        return meta
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/rows", response_model=PaginatedRows)
def rows(offset: int = 0, limit: int = 100):
    total, rows = ds.get_rows(offset, limit)
    return {"total": total, "offset": offset, "limit": limit, "rows": rows}
