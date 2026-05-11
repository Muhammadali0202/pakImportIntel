import shippo
from shippo.models import components
import logging
from config import settings

logger = logging.getLogger(__name__)

# Initialize the Shippo SDK
if settings.shippo_api_key:
    shippo_sdk = shippo.Shippo(api_key_header=settings.shippo_api_key)
else:
    logger.warning("Shippo API key not found. Shippo integration is disabled.")
    shippo_sdk = None

def create_address(name: str, company: str, street1: str, city: str, state: str, zip_code: str, country: str, phone: str, email: str):
    """Create an address in Shippo for shipping logic."""
    if not shippo_sdk:
        return {"error": "Shippo SDK is not configured."}
        
    try:
        response = shippo_sdk.addresses.create(
            components.AddressCreateRequest(
                name=name,
                company=company,
                street1=street1,
                city=city,
                state=state,
                zip=zip_code,
                country=country,
                phone=phone,
                email=email
            )
        )
        return response
    except Exception as e:
        logger.error(f"Error creating Shippo address: {e}")
        return {"error": str(e)}

def track_shipment(carrier: str, tracking_number: str):
    """Retrieve tracking details for a specific shipment."""
    if not shippo_sdk:
        return {"error": "Shippo SDK is not configured."}
        
    try:
        response = shippo_sdk.tracks.get_track(
            carrier=carrier,
            tracking_number=tracking_number
        )
        return response
    except Exception as e:
        logger.error(f"Error tracking shipment via Shippo: {e}")
        return {"error": str(e)}
