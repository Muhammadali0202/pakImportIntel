from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import HSCode
from agents.duty_agent import DutyAgent

router = APIRouter()
agent = DutyAgent()

class DutyRequest(BaseModel):
    cif_value: float
    origin: str
    product_hs_code: str
    is_filer: bool = True

@router.post("/estimate")
def estimate_duties(payload: DutyRequest, db: Session = Depends(get_db)):
    hs_data = db.query(HSCode).filter(HSCode.code == payload.product_hs_code).first()
    
    if not hs_data:
        raise HTTPException(status_code=404, detail=f"HS Code {payload.product_hs_code} not found in database.")
    
    hs_dict = {
        'cd_rate': hs_data.cd_rate,
        'rd_rate': hs_data.rd_rate,
        'acd_rate': hs_data.acd_rate,
        'st_rate': hs_data.st_rate,
        'wht_filer': hs_data.wht_filer,
        'wht_nonfiler': hs_data.wht_nonfiler
    }
    
    result = agent.calculate_duty(cif_usd=payload.cif_value, hs_data=hs_dict, is_filer=payload.is_filer)
    return {"breakdown": result["markdown"], "raw_data": result["raw_data"]}
