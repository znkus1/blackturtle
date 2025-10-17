from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models import Technology, TechnologyPublic, TechnologiesPublic

router = APIRouter()


@router.get("/", response_model=TechnologiesPublic)
def read_technologies(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    기술 목록 조회
    """
    count_statement = select(func.count()).select_from(Technology)
    count = session.exec(count_statement).one()

    statement = select(Technology).offset(skip).limit(limit)
    technologies = session.exec(statement).all()

    return TechnologiesPublic(data=technologies, count=count)


@router.get("/{technology_id}", response_model=TechnologyPublic)
def read_technology(session: SessionDep, technology_id: int) -> Any:
    """
    특정 기술 상세 조회
    """
    technology = session.get(Technology, technology_id)
    if not technology:
        raise HTTPException(status_code=404, detail="Technology not found")
    return technology