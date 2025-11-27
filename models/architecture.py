"""Data models for Azure architecture components."""

from typing import Optional
from pydantic import BaseModel, Field


class AzureService(BaseModel):
    """Represents an Azure service in the architecture."""
    
    service_name: str = Field(..., description="Azure service name (e.g., 'Azure App Service')")
    sku: str = Field(..., description="Service SKU/tier (e.g., 'Standard_S1')")
    quantity: int = Field(default=1, description="Number of instances")
    region: str = Field(..., description="Azure region")
    purpose: str = Field(..., description="Purpose of this service in the architecture")
    dependencies: list[str] = Field(default_factory=list, description="Service dependencies")


class ArchitecturePattern(BaseModel):
    """Represents an Azure architecture pattern."""
    
    pattern_name: str = Field(..., description="Name of the architecture pattern")
    description: str = Field(..., description="Description of the pattern")
    use_cases: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    considerations: list[str] = Field(default_factory=list)


class ArchitectureDocument(BaseModel):
    """Complete architecture document with bill of materials."""
    
    project_title: str = Field(..., description="Project title")
    architecture_pattern: str = Field(..., description="Chosen architecture pattern")
    services: list[AzureService] = Field(default_factory=list)
    networking: list[str] = Field(default_factory=list, description="Networking components")
    security: list[str] = Field(default_factory=list, description="Security measures")
    monitoring: list[str] = Field(default_factory=list, description="Monitoring and observability")
    deployment_notes: list[str] = Field(default_factory=list)
    alternatives_considered: list[str] = Field(default_factory=list)
    
    def add_service(self, service: AzureService) -> None:
        """Add a service to the architecture."""
        self.services.append(service)
    
    def get_services_by_type(self, service_type: str) -> list[AzureService]:
        """Get services filtered by type."""
        return [svc for svc in self.services if service_type.lower() in svc.service_name.lower()]
