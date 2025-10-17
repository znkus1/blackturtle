import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import date
from decimal import Decimal


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

# ============= BlackTurtle Models =============

# 1. 기업 정보
class Company(SQLModel, table=True):
    __tablename__ = "companies"
    
    company_id: int | None = Field(default=None, primary_key=True)
    id: str = Field(unique=True, max_length=50, index=True)
    name: str = Field(max_length=200, index=True)
    industry: str | None = Field(default=None, max_length=100)
    region: str | None = Field(default=None, max_length=50)
    location: str | None = Field(default=None, max_length=200)
    founded: int | None = None
    ceo: str | None = Field(default=None, max_length=100)
    website: str | None = Field(default=None, max_length=200)
    phone: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=100)
    description: str | None = None
    total_assets: Decimal | None = None
    employee_count: int | None = None
    
    financials: list["CompanyFinancial"] = Relationship(back_populates="company")
    technologies: list["Technology"] = Relationship(back_populates="company")


# 2. 기업 재무 정보 (시계열)
class CompanyFinancial(SQLModel, table=True):
    __tablename__ = "company_financials"
    
    financial_id: int | None = Field(default=None, primary_key=True)
    company_id: str = Field(foreign_key="companies.id", index=True)
    year: int = Field(index=True)
    revenue: Decimal | None = None
    assets: Decimal | None = None
    operating_profit: Decimal | None = None
    cost_of_sales: Decimal | None = None
    rd_investment: Decimal | None = None
    
    company: Company | None = Relationship(back_populates="financials")


# 3. 기술 정보
class Technology(SQLModel, table=True):
    __tablename__ = "technologies"
    
    technology_id: int | None = Field(default=None, primary_key=True)
    id: str = Field(unique=True, max_length=50, index=True)
    company_id: str = Field(foreign_key="companies.id", index=True)
    name: str = Field(max_length=300, index=True)
    description: str | None = None
    category: str | None = Field(default=None, max_length=100)
    
    # R&D 투자
    government_investment: Decimal | None = None
    company_investment: Decimal | None = None
    
    # 사업화 실적
    commercialization_revenue: Decimal | None = None
    
    # 기술 상세
    development_start_date: date | None = None
    development_end_date: date | None = None
    trl_level: int | None = Field(default=None, ge=1, le=9)
    commercialization_status: str | None = Field(default=None, max_length=50)
    market_size: Decimal | None = None
    verification_date: date | None = None
    verification_org: str | None = Field(default=None, max_length=200)
    patents_filed: int = Field(default=0)
    
    company: Company | None = Relationship(back_populates="technologies")


# API Response 스키마들
class CompanyPublic(SQLModel):
    company_id: int
    id: str
    name: str
    industry: str | None = None
    region: str | None = None


class CompaniesPublic(SQLModel):
    data: list[CompanyPublic]
    count: int


class TechnologyPublic(SQLModel):
    technology_id: int
    id: str
    name: str
    category: str | None = None
    government_investment: Decimal | None = None
    company_investment: Decimal | None = None
    commercialization_revenue: Decimal | None = None


class TechnologiesPublic(SQLModel):
    data: list[TechnologyPublic]
    count: int