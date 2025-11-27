"""Pricing Agent - Fetches and estimates Azure pricing."""

from agent_framework import ChatAgent, ChatMessage, Executor, WorkflowContext, handler
from models.architecture import ArchitectureDocument
from models.pricing import PricingEstimate, CostEstimate
from services.azure_pricing_service import AzurePricingService
from typing_extensions import Never
import json


class PricingAgent(Executor):
    """
    Agent responsible for generating pricing estimates.
    
    This agent:
    1. Analyzes the architecture document
    2. Fetches real pricing from Azure Retail Prices API
    3. Calculates cost estimates
    4. Provides cost optimization recommendations
    """
    
    agent: ChatAgent
    pricing_service: AzurePricingService
    
    def __init__(self, chat_client, id: str = "pricing_agent"):
        """
        Initialize the Pricing Agent.
        
        Args:
            chat_client: Azure AI chat client for creating the agent
            id: Executor ID
        """
        self.pricing_service = AzurePricingService()
        
        self.agent = chat_client.create_agent(
            instructions="""You are an expert Azure Cost Optimization Specialist.

Your role is to:
1. Calculate accurate pricing estimates for Azure architectures
2. Provide detailed cost breakdowns
3. Identify cost optimization opportunities
4. Suggest reserved instances or savings plans where applicable
5. Consider regional pricing differences

When calculating costs:
- Use actual Azure pricing data provided
- Calculate monthly costs based on 730 hours (24/7 operation)
- Consider scaling requirements
- Include all components (compute, storage, networking, etc.)
- Be transparent about assumptions

Output Format:
Return a JSON object with this structure:
{
  "project_title": "Project name",
  "region": "eastus",
  "cost_estimates": [
    {
      "service_name": "Azure App Service",
      "sku": "Standard_S1",
      "quantity": 2,
      "hours_per_month": 730,
      "unit_price": 0.10,
      "monthly_cost": 146.0,
      "annual_cost": 1752.0,
      "region": "eastus",
      "notes": ["Includes auto-scaling", "Consider reserved instances for 30% savings"]
    }
  ],
  "total_monthly_cost": 500.0,
  "total_annual_cost": 6000.0,
  "assumptions": ["24/7 operation", "Standard pricing tier", "No reserved instances"],
  "savings_opportunities": [
    "Save 30% with 1-year reserved instances",
    "Consider spot instances for dev/test workloads"
  ]
}

Provide actionable cost optimization recommendations.
""",
            model="gpt-4.1"
        )
        super().__init__(id=id)
    
    @handler
    async def calculate_pricing(
        self,
        architecture: ArchitectureDocument,
        ctx: WorkflowContext[Never, PricingEstimate]
    ) -> None:
        """
        Calculate pricing estimates for the architecture.
        
        Args:
            architecture: ArchitectureDocument from BOMAgent
            ctx: Workflow context to yield the pricing estimate
        """
        try:
            print(f"\n[PricingAgent] Calculating pricing for {len(architecture.services)} services")
            
            # Fetch pricing for each service
            pricing_data = []
            
            for service in architecture.services:
                print(f"[PricingAgent] Fetching pricing for {service.service_name} - {service.sku}")
                
                # Try to get pricing from Azure API
                pricing_item = None
                
                if "App Service" in service.service_name:
                    pricing_item = await self.pricing_service.get_app_service_pricing(
                        service.sku, service.region
                    )
                elif "SQL Database" in service.service_name or "SQL" in service.service_name:
                    pricing_item = await self.pricing_service.get_sql_database_pricing(
                        service.sku, service.region
                    )
                elif "Virtual Machine" in service.service_name or "VM" in service.service_name:
                    pricing_item = await self.pricing_service.get_vm_pricing(
                        service.sku, service.region
                    )
                else:
                    # Generic search
                    results = await self.pricing_service.search_prices(
                        service_name=service.service_name,
                        region=service.region,
                        sku_name=service.sku
                    )
                    pricing_item = results[0] if results else None
                
                if pricing_item:
                    pricing_data.append({
                        "service_name": service.service_name,
                        "sku": service.sku,
                        "quantity": service.quantity,
                        "region": service.region,
                        "unit_price": pricing_item.unit_price,
                        "unit_of_measure": pricing_item.unit_of_measure,
                        "purpose": service.purpose
                    })
                else:
                    print(f"[PricingAgent] No pricing found for {service.service_name}, using estimate")
                    # Use estimated pricing if API fails
                    pricing_data.append({
                        "service_name": service.service_name,
                        "sku": service.sku,
                        "quantity": service.quantity,
                        "region": service.region,
                        "unit_price": 0.10,  # Default estimate
                        "unit_of_measure": "1 Hour",
                        "purpose": service.purpose
                    })
            
            # Build the prompt with pricing data
            pricing_summary = "\n".join([
                f"- {p['service_name']} ({p['sku']}): ${p['unit_price']:.4f} per {p['unit_of_measure']}, Quantity: {p['quantity']}"
                for p in pricing_data
            ])
            
            prompt = f"""Calculate the total cost estimate for the following Azure architecture:

Project: {architecture.project_title}
Architecture Pattern: {architecture.architecture_pattern}
Region: {architecture.services[0].region if architecture.services else 'eastus'}

Services and Pricing:
{pricing_summary}

Additional Context:
- Networking: {', '.join(architecture.networking)}
- Security: {', '.join(architecture.security)}
- Monitoring: {', '.join(architecture.monitoring)}

Calculate detailed monthly and annual costs. Generate the pricing estimate in the JSON format specified in your instructions.
Include cost optimization recommendations and savings opportunities.
"""
            
            messages = [ChatMessage(role="user", text=prompt)]
            
            # Run the agent
            response = await self.agent.run(messages)
            response_text = response.text
            
            print(f"\n[PricingAgent] Response from agent:")
            print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
            
            # Parse the JSON response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            pricing_data_json = json.loads(response_text.strip())
            
            # Convert to PricingEstimate
            cost_estimates = [
                CostEstimate(**est) for est in pricing_data_json.get("cost_estimates", [])
            ]
            
            pricing = PricingEstimate(
                project_title=pricing_data_json.get("project_title", architecture.project_title),
                region=pricing_data_json.get("region", "eastus"),
                cost_estimates=cost_estimates,
                total_monthly_cost=pricing_data_json.get("total_monthly_cost", 0.0),
                total_annual_cost=pricing_data_json.get("total_annual_cost", 0.0),
                assumptions=pricing_data_json.get("assumptions", []),
                savings_opportunities=pricing_data_json.get("savings_opportunities", [])
            )
            
            print(f"\n[PricingAgent] Generated pricing estimate:")
            print(f"[PricingAgent] Monthly Cost: ${pricing.total_monthly_cost:.2f}")
            print(f"[PricingAgent] Annual Cost: ${pricing.total_annual_cost:.2f}")
            
            # Yield the pricing estimate
            await ctx.yield_output(pricing)
            
        except Exception as e:
            print(f"[PricingAgent] Error calculating pricing: {e}")
            # Create a minimal pricing estimate on error
            error_pricing = PricingEstimate(
                project_title=architecture.project_title,
                region="eastus",
                cost_estimates=[],
                total_monthly_cost=0.0,
                total_annual_cost=0.0,
                assumptions=[f"Error occurred: {str(e)}"],
                savings_opportunities=[]
            )
            await ctx.yield_output(error_pricing)
        
        finally:
            # Clean up the pricing service
            await self.pricing_service.close()
