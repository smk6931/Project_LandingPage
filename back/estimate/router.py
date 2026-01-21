from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Back.core.database import get_db
from Back.estimate.model import EstimateRequest, EstimateResponse
from Back.estimate.schema import EstimateCreate, EstimateDetail
from Back.estimate.service import capture_website, analyze_website_with_genai
import os
import asyncio

router = APIRouter(
    prefix="/api/estimate",
    tags=["Estimate"]
)

# 비동기 작업 함수
async def process_ai_analysis(request_id: int, db: AsyncSession):
    print(f"Starting AI analysis for request {request_id}")
    
    # DB 세션을 새로 생성해야 함 (BackgroundTasks는 별도 컨텍스트)
    # 하지만 여기선 주입받은 세션을 쓰면 이미 닫혀있을 수 있음.
    # 간단한 구현을 위해 여기서는 로직만 작성하고, 실제 운영에선 session factory를 써야 함.
    # 편의상 여기서는 넘겨받은 db 세션이 아직 유효하다고 가정하거나, 
    # 별도 처리가 필요하지만 일단 진행. (SQLAlchemy AsyncSession은 thread-safe하지 않음 주의)
    
    # 주의: BackgroundTasks에서 유효한 DB 세션을 얻으려면 
    # 별도의 dependency injection이 안되므로, 
    # sessionmaker를 직접 import해서 써야 할 수 있음.
    from Back.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(EstimateRequest).where(EstimateRequest.id == request_id))
            request = result.scalars().first()
            if not request:
                return
            request.status = "analyzing"
            await session.commit()
            
            try:
                # 1. 스크린샷
                screenshot_path = f"temp_{request_id}.png"
                await capture_website(request.reference_url, screenshot_path)
                
                # 2. AI 분석
                ai_result = await analyze_website_with_genai(screenshot_path, request.reference_url)
                
                if ai_result:
                    new_response = EstimateResponse(
                        request_id=request.id,
                        site_type=ai_result.get("site_type"),
                        page_count=ai_result.get("page_count"),
                        md_count=ai_result.get("md_count"),
                        estimated_cost_min=ai_result.get("estimated_cost_min"),
                        estimated_cost_max=ai_result.get("estimated_cost_max"),
                        estimated_days=ai_result.get("estimated_days"),
                        features=str(ai_result.get("features")),
                        scope_included=str(ai_result.get("scope_included")),
                        scope_excluded=str(ai_result.get("scope_excluded")),
                        special_notes=ai_result.get("special_notes"),
                        ai_analysis_raw=str(ai_result)
                    )
                    session.add(new_response)
                    request.status = "completed"
                else:
                    request.status = "failed"
                
                # 파일 삭제
                if os.path.exists(screenshot_path):
                    os.remove(screenshot_path)
                    
            except Exception as e:
                print(f"Analysis Error: {e}")
                request.status = "failed"
            
            await session.commit()

@router.post("/request")
async def create_estimate_request(
    request: EstimateCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # 1. DB 저장
    new_request = EstimateRequest(
        name=request.name,
        company=request.company,
        email=request.email,
        phone=request.phone,
        project_type=request.project_type,
        budget_range=request.budget_range,
        reference_url=str(request.reference_url),
        message=request.message,
        status="pending"
    )
    
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    
    # 2. 백그라운드 작업 예약
    background_tasks.add_task(process_ai_analysis, new_request.id, db)
    
    return {
        "success": True,
        "request_id": new_request.id,
        "message": "Request received. AI analysis started.",
        "status": "analyzing"
    }

@router.get("/{request_id}")
async def get_estimate(request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EstimateRequest).where(EstimateRequest.id == request_id))
    request = result.scalars().first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
        
    # 관계된 response도 가져와야 하지만, 일단 request 정보만 리턴 (Lazy loading 이슈 방지 위해 Eager loading 필요)
    # 간단 테스트용
    return request
