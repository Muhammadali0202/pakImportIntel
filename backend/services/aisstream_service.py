import asyncio
import websockets
import json
import logging
from db.database import SessionLocal
from db.models import Shipment
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def connect_ais_stream():
    uri = settings.aisstream_url
    api_key = settings.aisstream_key
    
    if not api_key:
        logger.warning("AISStream API key is not configured. Real-time tracking is disabled.")
        return

    # Subscribe to bounding box around Karachi to guarantee data flow for demo,
    # and specifically filter by our MMSIs if we only want our ships.
    db = SessionLocal()
    mmsi_list = []
    try:
        shipments = db.query(Shipment).filter(Shipment.mmsi.isnot(None)).all()
        mmsi_list = [s.mmsi for s in shipments]
    finally:
        db.close()

    # Bounding box around Karachi
    karachi_bbox = [[[23.0, 65.0], [26.0, 69.0]]]

    subscribe_message = {
        "APIKey": api_key,
        "BoundingBoxes": karachi_bbox,
        "FiltersShipMMSI": mmsi_list,
        "FilterMessageTypes": ["PositionReport"]
    }
    
    while True:
        try:
            logger.info("Connecting to AISStream...")
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps(subscribe_message))
                logger.info("Connected and subscribed to AISStream.")

                async for message in websocket:
                    data = json.loads(message)
                    if data.get("MessageType") == "PositionReport":
                        msg_data = data.get("Message", {}).get("PositionReport", {})
                        mmsi = str(data.get("MetaData", {}).get("MMSI"))
                        lat = msg_data.get("Latitude")
                        lon = msg_data.get("Longitude")
                        
                        # Only log matching MMSI or within our bbox for the demo
                        if mmsi in mmsi_list:
                            logger.info(f"Target Ship Update! MMSI: {mmsi}, Lat: {lat}, Lon: {lon}")
                            _update_shipment_location(mmsi, lat, lon)
                        else:
                            # For demo purposes, we log some traffic occasionally if needed
                            # logger.debug(f"General Traffic - MMSI: {mmsi}, Lat: {lat}, Lon: {lon}")
                            pass
        except websockets.exceptions.ConnectionClosed:
            logger.warning("AISStream connection closed. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"AISStream Error: {e}")
            await asyncio.sleep(5)

def _update_shipment_location(mmsi: str, lat: float, lon: float):
    db = SessionLocal()
    try:
        shipments = db.query(Shipment).filter(Shipment.mmsi == mmsi).all()
        for shipment in shipments:
            shipment.current_location = f"{lat}, {lon}"
        db.commit()
    except Exception as e:
        logger.error(f"Error updating shipment location: {e}")
    finally:
        db.close()
