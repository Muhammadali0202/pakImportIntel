from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Shipment

router = APIRouter()

@router.get("/")
def get_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return shipments

@router.get("/{shipment_id}")
def get_shipment(shipment_id: str, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    return shipment
