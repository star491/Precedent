from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any

class DecisionNode(BaseModel):
    """
    Represents a structured decision extracted from a document.
    """
    decision_title: str = Field(..., description="Short title of the decision made")
    decision_date: str = Field(..., description="Approximate date of the decision (YYYY-MM-DD)")
    team: str = Field(..., description="Team responsible (e.g., Engineering, Product)")
    rationale: List[str] = Field(..., description="Why this decision was made (bullet points)")
    alternatives: List[str] = Field(..., description="What other options were considered")
    outcome: Optional[str] = Field(None, description="Known outcome if this is a past decision")
    tags: List[str] = Field(default_factory=list, description="Keywords for filtering")
    source_file: str = Field(..., description="Name of the source document")

    @field_validator('rationale', mode='before')
    @classmethod
    def validate_rationale(cls, v):
        if isinstance(v, str):
            return [v]
        return v

class SearchQuery(BaseModel):
    query: str
    filter_team: Optional[str] = None
    filter_year: Optional[int] = None
    limit: int = 5

class SearchResult(BaseModel):
    score: float
    decision: DecisionNode
    context: str = Field(..., description="Relevant snippet from the source text")
