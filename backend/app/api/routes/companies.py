from typing import Any
import uuid

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Company, CompanyPublic, CompaniesPublic

router = APIRouter()


@router.get("/", response_model=CompaniesPublic)
def read_companies(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    기업 목록 조회
    """
    count_statement = select(func.count()).select_from(Company)
    count = session.exec(count_statement).one()

    statement = select(Company).offset(skip).limit(limit)
    companies = session.exec(statement).all()

    return CompaniesPublic(data=companies, count=count)


@router.get("/{company_id}", response_model=CompanyPublic)
def read_company(session: SessionDep, company_id: int) -> Any:
    """
    특정 기업 상세 조회
    """
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company