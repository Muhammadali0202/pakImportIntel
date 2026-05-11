from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class Shipment(Base):
    __tablename__ = "shipments"
    
    id = Column(String, primary_key=True, index=True)
    status = Column(String)
    origin_city = Column(String)
    origin_country = Column(String)
    destination_city = Column(String)
    destination_port = Column(String)
    vessel_name = Column(String)
    container_number = Column(String)
    eta = Column(String)
    delay_days = Column(Integer, default=0)
    delay_reason = Column(String)
    customs_status = Column(String)
    declared_value_usd = Column(Float)
    hs_code = Column(String)
    product_description = Column(String)
    mmsi = Column(String, nullable=True)
    current_location = Column(String, nullable=True)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, default='demo_user')
    shipment_id = Column(String)
    filename = Column(String)
    doc_type = Column(String)
    file_path = Column(String)
    parsed_text = Column(String)
    embedding_status = Column(String)

class HSCode(Base):
    __tablename__ = "hs_codes"
    
    code = Column(String, primary_key=True, index=True)
    description = Column(String)
    cd_rate = Column(Float)
    rd_rate = Column(Float, default=0)
    acd_rate = Column(Float, default=7)
    st_rate = Column(Float, default=18)
    wht_filer = Column(Float, default=5.5)
    wht_nonfiler = Column(Float, default=8)
    notes = Column(String)
