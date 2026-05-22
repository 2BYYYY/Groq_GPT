from pydantic import BaseModel
from typing import Optional, List 

class ESbotRequest(BaseModel):
    query: str
    
class ProfileItem(BaseModel):
    title: str 
    description: Optional[str] = None 
    issuer: Optional[str] = None 
    organization: Optional[str] = None 
    category: str 
    duration: Optional[str] = None

class StudentProfile(BaseModel):
    bio: str 
    gwa: float 
    highest_degree: str 
    date_of_birth: str
    annual_family_income: float 
    special_group: Optional[str] = None 
    profile_items: List[ProfileItem]

class Scholarship(BaseModel):
    program_name: str 
    status: str 
    grant_type: str 
    deadline: str 
    cutoff_grade: float 
    description: str 
    annual_family_income: Optional[float] = None 
    eligibility: str 
    e_recommend: float 
    match: str

class ScoreBreakdown(BaseModel):
    eligibility: float
    academic: float
    income: float
    bonus: float
    profile: float

class LLMAnalysisPayload(BaseModel):
    student: StudentProfile 
    scholarship: Scholarship
    breakdown: ScoreBreakdown