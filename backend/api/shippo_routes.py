from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.shippo_service import create_address, track_shipment

router = APIRouter()

class AddressPayload(BaseModel):
    name: str
    company: str
    street1: str
    city: str
    state: str
    zip_code: str
    country: str
    phone: str
    email: str

@router.post("/address")
def add_shippo_address(payload: AddressPayload):
    """Create a new origin or destination address in Shippo."""
    response = create_address(
        name=payload.name,
        company=payload.company,
        street1=payload.street1,
        city=payload.city,
        state=payload.state,
        zip_code=payload.zip_code,
        country=payload.country,
        phone=payload.phone,
        email=payload.email
    )
    if isinstance(response, dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.get("/track/{carrier}/{tracking_number}")
def track_shippo_shipment(carrier: str, tracking_number: str):
    """Track a shipment via Shippo API."""
    response = track_shipment(carrier, tracking_number)
    if isinstance(response, dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
