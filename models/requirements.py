"""Data models for customer requirements and specifications."""

from typing import Optional
from pydantic import BaseModel, Field


class CustomerRequirement(BaseModel):
    """Represents a single customer requirement."""
    
    requirement_id: str = Field(..., description="Unique identifier for the requirement")
    description: str = Field(..., description="Description of the requirement")
    category: str = Field(..., description="Category (functional, non-functional, technical)")
    priority: str = Field(default="medium", description="Priority level (high, medium, low)")
    clarification_needed: bool = Field(default=False, description="Whether clarification is needed")


class SpecificationDocument(BaseModel):
    """Complete specification document for customer needs."""
    
    customer_name: Optional[str] = Field(None, description="Customer organization name")
    project_title: str = Field(..., description="Project title")
    summary: str = Field(..., description="High-level summary of the project")
    requirements: list[CustomerRequirement] = Field(default_factory=list)
    clarifying_questions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    target_users: Optional[int] = Field(None, description="Estimated number of users")
    target_region: str = Field(default="eastus", description="Preferred Azure region")
    
    def add_requirement(self, req: CustomerRequirement) -> None:
        """Add a requirement to the specification."""
        self.requirements.append(req)
    
    def get_requirements_by_priority(self, priority: str) -> list[CustomerRequirement]:
        """Get requirements filtered by priority."""
        return [req for req in self.requirements if req.priority == priority]
