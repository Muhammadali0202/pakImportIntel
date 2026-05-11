import json
import csv
import os
import sys

# Ensure we can import from the root backend dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, Base
from db.models import Shipment, Document, HSCode

# Make sure tables are created
Base.metadata.create_all(bind=engine)

def seed_shipments():
    db: Session = SessionLocal()
    
    # Check if shipments already exist
    count = db.query(Shipment).count()
    if count > 0:
        print("Shipments table already seeded.")
        db.close()
        return

    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mock_shipments.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for item in data:
            shipment = Shipment(
                id=item.get("id"),
                status=item.get("status"),
                origin_city=item.get("origin_city"),
                origin_country=item.get("origin_country"),
                destination_city=item.get("destination_city"),
                destination_port=item.get("destination_port"),
                vessel_name=item.get("vessel_name"),
                container_number=item.get("container_number"),
                eta=item.get("eta"),
                delay_days=item.get("delay_days", 0),
                delay_reason=item.get("delay_reason", ""),
                customs_status=item.get("customs_status"),
                declared_value_usd=item.get("declared_value_usd"),
                hs_code=item.get("hs_code"),
                product_description=item.get("product_description"),
                mmsi=item.get("mmsi")
            )
            db.add(shipment)
            
        db.commit()
        print(f"Successfully seeded {len(data)} shipments.")
    except Exception as e:
        print(f"Error seeding shipments: {e}")
        db.rollback()
    finally:
        db.close()

def seed_hscodes():
    db: Session = SessionLocal()
    count = db.query(HSCode).count()
    if count > 0:
        print("HS Codes table already seeded.")
        db.close()
        return

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hs_codes.csv')
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                hs = HSCode(
                    code=row['code'],
                    description=row['description'],
                    cd_rate=float(row['cd_rate']),
                    rd_rate=float(row['rd_rate']),
                    acd_rate=float(row['acd_rate']),
                    st_rate=float(row['st_rate']),
                    wht_filer=float(row['wht_filer']),
                    wht_nonfiler=float(row['wht_nonfiler']),
                    notes=row['notes']
                )
                db.add(hs)
        db.commit()
        print("Successfully seeded HS codes.")
    except Exception as e:
        print(f"Error seeding HS codes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_shipments()
    seed_hscodes()
