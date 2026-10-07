from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import hashlib
import uuid
import qrcode
import os
from schemas import (
    UserRegister,
    UserLogin,
    InstrumentCreate,
    InspectionCreate,
    CertificateCreate,
    VerificationDecision,
    RenewalRequest
)
from database import Base, engine, get_db
from models import User, Instrument, Inspection, Certificate
from auth import create_token

app = FastAPI(
    title="Veri-X API",
    description="SIH 26036 - Online Verification System",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


# -------------------------
# SCHEMAS
# -------------------------

class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    role: str = "applicant"


class Login(BaseModel):
    email: str
    password: str


class InstrumentCreate(BaseModel):
    owner_name: str
    type: str
    manufacturer: str
    capacity: str
    district: str


class InspectionCreate(BaseModel):
    instrument_id: str
    officer: str
    result: str
    remarks: str


# -------------------------
# HOME
# -------------------------

@app.get("/")
def home():

    return {
        "project": "Veri-X",
        "problem_statement": "26036",
        "status": "Backend Running",
        "message": "Veri-X API is operational"
    }


# -------------------------
# REGISTER
# -------------------------

@app.post("/auth/register")
def register(
    data: RegisterUser,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user = User(
        name=data.name,
        email=data.email,
        password=data.password,
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user_id": user.id
    }


# -------------------------
# LOGIN
# -------------------------

@app.post("/auth/login")
def login(
    data: Login,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user or user.password != data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_token(
        user.id,
        user.role
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


# -------------------------
# REGISTER INSTRUMENT
# -------------------------

@app.post("/instruments")
def create_instrument(
    data: InstrumentCreate,
    db: Session = Depends(get_db)
):

    instrument_id = "VX-" + uuid.uuid4().hex[:10].upper()

    instrument = Instrument(
        instrument_id=instrument_id,
        owner_name=data.owner_name,
        type=data.type,
        manufacturer=data.manufacturer,
        capacity=data.capacity,
        district=data.district
    )

    db.add(instrument)
    db.commit()
    db.refresh(instrument)

    return {
        "message": "Instrument registered",
        "instrument_id": instrument_id,
        "status": "Registered"
    }


# -------------------------
# GET INSTRUMENTS
# -------------------------

@app.get("/instruments")
def get_instruments(
    db: Session = Depends(get_db)
):

    return db.query(Instrument).all()


# -------------------------
# FIELD INSPECTION
# -------------------------

@app.post("/inspections")
def create_inspection(
    data: InspectionCreate,
    db: Session = Depends(get_db)
):

    raw_data = (
        data.instrument_id +
        data.officer +
        data.result +
        data.remarks
    )

    data_hash = hashlib.sha256(
        raw_data.encode()
    ).hexdigest()

    inspection = Inspection(
        instrument_id=data.instrument_id,
        officer=data.officer,
        result=data.result,
        remarks=data.remarks,
        data_hash=data_hash
    )

    db.add(inspection)

    instrument = db.query(Instrument).filter(
        Instrument.instrument_id == data.instrument_id
    ).first()

    if instrument:
        instrument.status = data.result

    db.commit()

    return {
        "message": "Inspection submitted",
        "integrity_hash": data_hash,
        "status": data.result
    }


# -------------------------
# GENERATE CERTIFICATE
# -------------------------

@app.post("/certificates/{instrument_id}")
def generate_certificate(
    instrument_id: str,
    db: Session = Depends(get_db)
):

    instrument = db.query(Instrument).filter(
        Instrument.instrument_id == instrument_id
    ).first()

    if not instrument:
        raise HTTPException(
            status_code=404,
            detail="Instrument not found"
        )

    certificate_id = "CERT-" + uuid.uuid4().hex[:10].upper()

    certificate_data = (
        certificate_id +
        instrument.instrument_id +
        instrument.owner_name
    )

    integrity_hash = hashlib.sha256(
        certificate_data.encode()
    ).hexdigest()

    certificate = Certificate(
        certificate_id=certificate_id,
        instrument_id=instrument.instrument_id,
        owner_name=instrument.owner_name,
        district=instrument.district,
        valid_until="2027-09-19",
        integrity_hash=integrity_hash
    )

    db.add(certificate)

    instrument.status = "Verified"

    db.commit()

    # QR generation
    os.makedirs("qr_codes", exist_ok=True)

    qr_data = (
    f"https://verifyx-backend-s31f.onrender.com/verify/"
    f"{certificate_id}"
)
    

    img = qrcode.make(qr_data)

    img.save(
        f"qr_codes/{certificate_id}.png"
    )

    return {
        "certificate_id": certificate_id,
        "instrument_id": instrument.instrument_id,
        "qr": f"/qr_codes/{certificate_id}.png",
        "integrity_hash": integrity_hash,
        "status": "VALID"
    }


# -------------------------
# PUBLIC QR VERIFICATION
# -------------------------

@app.get("/verify/{certificate_id}")
def verify_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):

    certificate = db.query(Certificate).filter(
        Certificate.certificate_id == certificate_id
    ).first()

    if not certificate:
        return {
            "valid": False,
            "message": "Certificate not found"
        }

    raw_data = (
        certificate.certificate_id +
        certificate.instrument_id +
        certificate.owner_name
    )

    calculated_hash = hashlib.sha256(
        raw_data.encode()
    ).hexdigest()

    integrity_valid = (
        calculated_hash ==
        certificate.integrity_hash
    )

    return {
        "valid": integrity_valid,
        "certificate_id": certificate.certificate_id,
        "instrument_id": certificate.instrument_id,
        "owner": certificate.owner_name,
        "district": certificate.district,
        "status": certificate.status,
        "valid_until": certificate.valid_until,
        "integrity_verified": integrity_valid
    }


# -------------------------
# DASHBOARD
# -------------------------

@app.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    instruments = db.query(
        Instrument
    ).all()

    total = len(instruments)

    verified = len([
        x for x in instruments
        if x.status == "Verified"
    ])

    pending = len([
        x for x in instruments
        if x.status == "Registered"
    ])

    return {
        "total_instruments": total,
        "verified": verified,
        "pending": pending,
        "compliance_percentage":
            round((verified / total) * 100, 2)
            if total else 0
    }