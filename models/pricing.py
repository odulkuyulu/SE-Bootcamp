"""Data models for Azure pricing information."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PricingItem(BaseModel):
    """Represents a single pricing item from Azure Retail Prices API."""
    
    service_name: str = Field(..., description="Azure service name")
    sku_name: str = Field(..., description="SKU name")
    region: str = Field(..., description="Azure region")
    unit_price: float = Field(..., description="Unit price in USD")
    unit_of_measure: str = Field(..., description="Unit of measure (e.g., '1 Hour')")
    retail_price: float = Field(..., description="Retail price")
    currency_code: str = Field(default="USD", description="Currency code")
    tier_minimum_units: Optional[float] = Field(None, description="Tier minimum units")
    product_name: str = Field(..., description="Product name")
    meter_name: str = Field(..., description="Meter name")


class CostEstimate(BaseModel):
    """Represents a cost estimate for a service."""
    
    service_name: str = Field(..., description="Azure service name")
    sku: str = Field(..., description="SKU/tier")
    quantity: int = Field(default=1, description="Number of instances")
    hours_per_month: int = Field(default=730, description="Hours per month (730 = 24/7)")
    unit_price: float = Field(..., description="Price per unit")
    monthly_cost: float = Field(..., description="Estimated monthly cost")
    annual_cost: float = Field(..., description="Estimated annual cost")
    region: str = Field(..., description="Azure region")
    notes: list[str] = Field(default_factory=list, description="Additional notes")


class PricingEstimate(BaseModel):
    """Complete pricing estimate for an architecture."""
    
    project_title: str = Field(..., description="Project title")
    estimate_date: datetime = Field(default_factory=datetime.now)
    region: str = Field(..., description="Primary Azure region")
    cost_estimates: list[CostEstimate] = Field(default_factory=list)
    total_monthly_cost: float = Field(default=0.0, description="Total monthly cost")
    total_annual_cost: float = Field(default=0.0, description="Total annual cost")
    assumptions: list[str] = Field(default_factory=list)
    savings_opportunities: list[str] = Field(default_factory=list)
    
    def add_cost_estimate(self, estimate: CostEstimate) -> None:
        """Add a cost estimate and update totals."""
        self.cost_estimates.append(estimate)
        self.total_monthly_cost += estimate.monthly_cost
        self.total_annual_cost += estimate.annual_cost
    
    def get_cost_breakdown(self) -> dict[str, float]:
        """Get cost breakdown by service."""
        breakdown = {}
        for est in self.cost_estimates:
            breakdown[est.service_name] = est.monthly_cost
        return breakdown
