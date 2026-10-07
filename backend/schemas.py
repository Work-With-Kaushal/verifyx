from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ============================================================
# AUTHENTICATION
# ============================================================

class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: str = "applicant"
    district: str = ""


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    district: str

    class Config:
        from_attributes = True


# ============================================================
# INSTRUMENT
# ============================================================

class InstrumentCreate(BaseModel):
    owner_name: str
    instrument_type: str
    manufacturer: str = ""
    capacity: str = ""
    district: str


class InstrumentResponse(BaseModel):
    id: int
    instrument_id: str
    owner_name: str
    instrument_type: str
    manufacturer: str
    capacity: str
    district: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# APPLICATION
# ============================================================

class ApplicationCreate(BaseModel):
    instrument_id: int
    applicant_name: str
    district: str
    remarks: Optional[str] = ""


class ApplicationResponse(BaseModel):
    id: int
    application_id: str
    instrument_id: int
    applicant_name: str
    district: str
    remarks: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# OFFICER ASSIGNMENT
# ============================================================

class AssignmentCreate(BaseModel):
    application_id: int
    officer_name: str
    inspection_date: datetime


class AssignmentResponse(BaseModel):
    id: int
    application_id: int
    officer_name: str
    inspection_date: datetime
    status: str

    class Config:
        from_attributes = True


# ============================================================
# INSPECTION
# ============================================================

class InspectionCreate(BaseModel):
    instrument_id: int
    officer: str
    result: str
    remarks: str = ""
    photo_url: str = ""
    client_id: Optional[str] = None


class InspectionResponse(BaseModel):
    id: int
    instrument_id: int
    officer: str
    result: str
    remarks: str
    photo_url: str
    data_hash: str
    synced: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# CERTIFICATE
# ============================================================

class CertificateCreate(BaseModel):
    instrument_id: int
    valid_until: datetime


class CertificateResponse(BaseModel):
    certificate_id: str
    instrument_id: int
    owner_name: str
    district: str
    status: str
    valid_until: datetime
    integrity_hash: str
    qr_url: str = ""

    class Config:
        from_attributes = True


# ============================================================
# CERTIFICATE RENEWAL
# ============================================================

class RenewalRequest(BaseModel):
    certificate_id: str
    new_valid_until: datetime


# ============================================================
# VERIFICATION DECISION
# ============================================================

# ============================================================
# VERIFICATION DECISION
# ============================================================

# ============================================================
# VERIFICATION DECISION
# ============================================================

class VerificationDecision(BaseModel):
    decision: str
    remarks: str = ""


# Backward-compatible name
class DecisionRequest(BaseModel):
    decision: str
    remarks: str = ""

# ============================================================
# QR VERIFICATION
# ============================================================

class QRVerificationResponse(BaseModel):
    valid: bool
    certificate_id: Optional[str] = None
    instrument_id: Optional[str] = None
    owner: Optional[str] = None
    district: Optional[str] = None
    status: Optional[str] = None
    valid_until: Optional[datetime] = None
    integrity_verified: bool = False
    message: str


# ============================================================
# DASHBOARD
# ============================================================

class DashboardResponse(BaseModel):
    total_instruments: int
    verified: int
    pending: int
    rejected: int
    compliance_percentage: float


# ============================================================
# DISTRICT DASHBOARD
# ============================================================

class DistrictSummary(BaseModel):
    district: str
    total: int
    verified: int
    pending: int
    rejected: int
    compliance_percentage: float