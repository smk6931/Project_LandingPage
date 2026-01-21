from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from Back.core.database import Base

class EstimateRequest(Base):
    __tablename__ = "estimate_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    company = Column(String(200), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    
    # 프로젝트 정보
    project_type = Column(String(50), nullable=False)  # imweb, custom, etc
    budget_range = Column(String(50), nullable=True)
    reference_url = Column(Text, nullable=False)  # AI 분석 대상 URL
    message = Column(Text, nullable=False)
    
    # 상태 관리
    status = Column(String(20), default="pending")  # pending, analyzing, completed, failed
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 견적서 (1:1)
    response = relationship("EstimateResponse", back_populates="request", uselist=False)

class EstimateResponse(Base):
    __tablename__ = "estimate_responses"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("estimate_requests.id"), nullable=False)
    
    # 분석 결과
    site_type = Column(String(50), nullable=True)  # 원페이지, 멀티페이지 등
    page_count = Column(Integer, nullable=True)
    md_count = Column(Float, nullable=True)  # 소요 MD (Man-Day)
    
    # 금액 및 일정
    estimated_cost_min = Column(Integer, nullable=True)  # 만원 단위
    estimated_cost_max = Column(Integer, nullable=True)  # 만원 단위
    estimated_days = Column(Integer, nullable=True)      # 일 단위
    
    # 상세 내용
    features = Column(Text, nullable=True)       # 기능 목록 (JSON string)
    scope_included = Column(Text, nullable=True) # 포함 범위
    scope_excluded = Column(Text, nullable=True) # 제외 범위
    special_notes = Column(Text, nullable=True)  # 특이사항 (AI 조언)
    
    created_at = Column(DateTime, default=datetime.now)

    # 관계 설정
    request = relationship("EstimateRequest", back_populates="response")
