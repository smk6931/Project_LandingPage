from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# === 요청 (Request) 스키마 ===
class EstimateCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    company: Optional[str] = None
    email: EmailStr
    phone: str
    project_type: str
    budget_range: Optional[str] = None
    reference_url: HttpUrl
    message: str

class EstimateResponseBase(BaseModel):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# === 응답 (Response) 스키마 (AI 분석 결과) ===
class AIAnalysisResult(BaseModel):
    site_type: str
    page_count: int
    md_count: float
    estimated_cost_min: int
    estimated_cost_max: int
    estimated_days: int
    features: List[str]
    scope_included: List[str]
    scope_excluded: List[str]
    special_notes: str

# === 최종 API 응답 스키마 ===
class EstimateDetail(EstimateResponseBase):
    name: str
    reference_url: HttpUrl
    analysis: Optional[AIAnalysisResult] = None
