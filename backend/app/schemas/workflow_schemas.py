from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    idea: str = Field(..., min_length=10)
    audience: Optional[str] = None
    industry: Optional[str] = None
    problem: Optional[str] = None


class ProjectUpdate(BaseModel):
    idea: Optional[str] = Field(default=None, min_length=10)
    audience: Optional[str] = None
    industry: Optional[str] = None
    problem: Optional[str] = None


class ProjectRecord(BaseModel):
    project_id: str
    idea: str
    audience: Optional[str] = None
    industry: Optional[str] = None
    problem: Optional[str] = None
    workflow_stage: str = "discover"
    discovery: Dict[str, Any] = {}
    positioning: Dict[str, Any] = {}
    brand_definition: Dict[str, Any] = {}
    expression: Dict[str, Any] = {}
    challenge: Dict[str, Any] = {}
    final_brand_system: Dict[str, Any] = {}
    launch: Dict[str, Any] = {}
    created_at: str
    updated_at: str


class StageResponse(BaseModel):
    project_id: str
    stage: str
    data: Dict[str, Any]
    workflow_stage: str


class ExportResponse(BaseModel):
    project_id: str
    final_brand_system: Dict[str, Any]
    html_export: str
    markdown_export: str
