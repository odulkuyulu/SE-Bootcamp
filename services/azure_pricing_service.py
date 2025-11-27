"""Azure Retail Prices API client service."""

import httpx
from typing import Optional
from models.pricing import PricingItem


class AzurePricingService:
    """Service for interacting with Azure Retail Prices API."""
    
    def __init__(
        self,
        base_url: str = "https://prices.azure.com/api/retail/prices",
        api_version: str = "2023-01-01-preview"
    ):
        self.base_url = base_url
        self.api_version = api_version
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_prices(
        self,
        service_name: Optional[str] = None,
        region: Optional[str] = None,
        sku_name: Optional[str] = None,
        currency: str = "USD"
    ) -> list[PricingItem]:
        """
        Search Azure retail prices with filters.
        
        Args:
            service_name: Filter by service name (e.g., "Virtual Machines")
            region: Filter by region (e.g., "eastus")
            sku_name: Filter by SKU name (e.g., "Standard_D2s_v3")
            currency: Currency code (default: USD)
        
        Returns:
            List of PricingItem objects
        """
        # Build OData filter query
        filters = []
        
        if service_name:
            filters.append(f"serviceName eq '{service_name}'")
        
        if region:
            filters.append(f"armRegionName eq '{region}'")
        
        if sku_name:
            filters.append(f"contains(skuName, '{sku_name}')")
        
        filters.append(f"currencyCode eq '{currency}'")
        filters.append("priceType eq 'Consumption'")  # Focus on pay-as-you-go pricing
        
        filter_query = " and ".join(filters)
        
        params = {
            "$filter": filter_query,
            "api-version": self.api_version
        }
        
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            items = data.get("Items", [])
            
            pricing_items = []
            for item in items[:50]:  # Limit to first 50 results
                try:
                    pricing_item = PricingItem(
                        service_name=item.get("serviceName", ""),
                        sku_name=item.get("skuName", ""),
                        region=item.get("armRegionName", ""),
                        unit_price=float(item.get("unitPrice", 0.0)),
                        unit_of_measure=item.get("unitOfMeasure", ""),
                        retail_price=float(item.get("retailPrice", 0.0)),
                        currency_code=item.get("currencyCode", "USD"),
                        tier_minimum_units=item.get("tierMinimumUnits"),
                        product_name=item.get("productName", ""),
                        meter_name=item.get("meterName", "")
                    )
                    pricing_items.append(pricing_item)
                except Exception as e:
                    print(f"Error parsing pricing item: {e}")
                    continue
            
            return pricing_items
        
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return []
    
    async def get_vm_pricing(self, vm_size: str, region: str = "eastus") -> Optional[PricingItem]:
        """Get pricing for a specific VM size."""
        results = await self.search_prices(
            service_name="Virtual Machines",
            region=region,
            sku_name=vm_size
        )
        return results[0] if results else None
    
    async def get_app_service_pricing(self, sku: str, region: str = "eastus") -> Optional[PricingItem]:
        """Get pricing for Azure App Service."""
        results = await self.search_prices(
            service_name="Azure App Service",
            region=region,
            sku_name=sku
        )
        return results[0] if results else None
    
    async def get_sql_database_pricing(self, sku: str, region: str = "eastus") -> Optional[PricingItem]:
        """Get pricing for Azure SQL Database."""
        results = await self.search_prices(
            service_name="SQL Database",
            region=region,
            sku_name=sku
        )
        return results[0] if results else None
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
