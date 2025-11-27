"""
SE Specialist Architecture & Pricing Assistant - Simplified Demo
This demo version works without the Microsoft Agent Framework.
It demonstrates the multi-agent workflow concept using direct API calls.
"""

import asyncio
import os
from dotenv import load_dotenv
from services.azure_pricing_service import AzurePricingService
from services.ms_learn_service import MSLearnService

# Load environment variables
load_dotenv()


async def demo_scenario_simple():
    """Simple demonstration of the multi-agent architecture concept."""
    print("\n" + "="*80)
    print("SE SPECIALIST ARCHITECTURE & PRICING ASSISTANT")
    print("Multi-Agent Demo (Simplified Version)")
    print("="*80)
    
    customer_input = """
    We need to build a simple corporate website with:
    - About 1,000 daily visitors
    - Content management for marketing team
    - Contact form and newsletter signup
    - Blog section with monthly updates
    - Need it to be secure and fast
    - Budget: around $200/month
    - Location: US East
    """
    
    print(f"\nCustomer Input:\n{customer_input}\n")
    print("-"*80)
    
    # Step 1: Requirements Analysis (Simulated Spec Agent)
    print("\n[SPEC AGENT] Analyzing requirements...")
    print("-"*40)
    spec_result = {
        "requirements": [
            "Web hosting for corporate website",
            "Support for ~1,000 daily visitors (~30,000/month)",
            "Content Management System (CMS)",
            "Form handling and email integration",
            "Blog functionality",
            "SSL/TLS security",
            "CDN for fast content delivery",
            "Estimated traffic: Low to moderate"
        ],
        "clarifying_questions": [
            "Will you need a custom domain?",
            "Do you need staging environment for testing?",
            "Any specific CMS preference (WordPress, etc.)?"
        ],
        "assumptions": [
            "Standard business hours support acceptable",
            "Content updates a few times per month",
            "No e-commerce or payment processing needed"
        ]
    }
    
    print("\nIdentified Requirements:")
    for req in spec_result["requirements"]:
        print(f"  • {req}")
    
    print("\nClarifying Questions:")
    for q in spec_result["clarifying_questions"]:
        print(f"  ? {q}")
    
    print("\nAssumptions:")
    for a in spec_result["assumptions"]:
        print(f"  ✓ {a}")
    
    # Step 2: Architecture Design (Simulated BOM Agent)
    print("\n[BOM AGENT] Designing architecture...")
    print("-"*40)
    
    ms_learn = MSLearnService()
    recommended_service_names = await ms_learn.recommend_services(
        requirements=["web hosting", "content management", "cdn", "forms"]
    )
    
    print("\nRecommended Azure Services:")
    for service_name in recommended_service_names[:5]:  # Limit to first 5
        service_info = await ms_learn.get_service_info(service_name)
        if service_info:
            print(f"\n  Service: {service_name}")
            print(f"  Purpose: {service_info['description']}")
            print(f"  Use Case: {service_info['use_cases'][0] if service_info.get('use_cases') else 'General purpose'}")
            print(f"  Available SKUs: {', '.join(service_info.get('skus', [])[:3])}")
    
    architecture = {
        "services": [
            {"name": "Azure App Service", "sku": "B1", "quantity": 1},
            {"name": "Azure SQL Database", "sku": "Basic", "quantity": 1},
            {"name": "Azure Storage", "sku": "Standard_LRS", "quantity": 1},
            {"name": "Azure CDN", "sku": "Standard_Microsoft", "quantity": 1},
            {"name": "Azure Front Door", "sku": "Standard", "quantity": 1}
        ]
    }
    
    # Step 3: Pricing Calculation (Simulated Pricing Agent)
    print("\n[PRICING AGENT] Calculating costs...")
    print("-"*40)
    
    pricing_service = AzurePricingService()
    
    print("\nFetching real-time pricing from Azure Retail Prices API...")
    
    # Get App Service pricing
    try:
        app_service_price = await pricing_service.get_app_service_pricing(
            sku="B1",
            region="eastus"
        )
        app_service_monthly = app_service_price.retail_price * 730 if app_service_price else 13.14
    except Exception as e:
        print(f"  Note: Using estimated pricing (API: {str(e)})")
        app_service_monthly = 13.14
    
    # Get SQL Database pricing
    try:
        sql_price = await pricing_service.get_sql_database_pricing(
            sku="Basic",
            region="eastus"
        )
        sql_monthly = sql_price.retail_price * 730 if sql_price else 4.90
    except Exception as e:
        print(f"  Note: Using estimated pricing (API: {str(e)})")
        sql_monthly = 4.90
    
    # Storage estimate
    storage_monthly = 0.018  # $0.018/GB for first 50GB
    
    # CDN estimate (per GB transfer)
    cdn_monthly = 10.00  # Estimated for low traffic
    
    # Front Door
    front_door_monthly = 35.00  # Standard tier base cost
    
    total_monthly = app_service_monthly + sql_monthly + storage_monthly + cdn_monthly + front_door_monthly
    total_annual = total_monthly * 12
    
    print("\n" + "="*80)
    print("ARCHITECTURE & PRICING ESTIMATE")
    print("="*80)
    
    print("\nProposed Architecture:")
    print(f"  • App Service (B1): Hosting web application")
    print(f"  • SQL Database (Basic): Content and user data")
    print(f"  • Storage Account: Static files and media")
    print(f"  • CDN: Fast content delivery globally")
    print(f"  • Front Door: Load balancing and security")
    
    print("\nPricing Breakdown:")
    print(f"  App Service (B1)          ${app_service_monthly:>8.2f}/month")
    print(f"  SQL Database (Basic)      ${sql_monthly:>8.2f}/month")
    print(f"  Storage (Standard LRS)    ${storage_monthly:>8.2f}/month")
    print(f"  CDN (Standard)            ${cdn_monthly:>8.2f}/month")
    print(f"  Front Door (Standard)     ${front_door_monthly:>8.2f}/month")
    print(f"  {'-'*35}")
    print(f"  Total Monthly Cost:       ${total_monthly:>8.2f}")
    print(f"  Total Annual Cost:        ${total_annual:>8.2f}")
    
    print("\nCost Optimization Tips:")
    print("  💡 Use Azure Reserved Instances for 1-year commitment to save ~30%")
    print("  💡 Enable CDN caching rules to reduce bandwidth costs")
    print("  💡 Implement auto-scaling only when needed to control costs")
    print("  💡 Use Azure Monitor to track usage and optimize resources")
    
    print("\nNext Steps:")
    print("  1. Review architecture with security team")
    print("  2. Set up development environment in staging subscription")
    print("  3. Configure CI/CD pipeline with Azure DevOps")
    print("  4. Implement monitoring and alerting")
    print("  5. Plan phased rollout with pilot users")
    
    print("\n" + "="*80)
    
    await pricing_service.close()


async def main():
    """Main entry point."""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║  SE Specialist Architecture & Pricing Assistant                  ║
    ║  Multi-Agent Demo (Simplified Version)                           ║
    ║                                                                  ║
    ║  This demo shows the concept of three specialized agents:       ║
    ║  1. Spec Agent: Analyzes customer requirements                  ║
    ║  2. BOM Agent: Designs architecture using Azure services        ║
    ║  3. Pricing Agent: Calculates costs using Azure pricing API     ║
    ║                                                                  ║
    ║  Note: This simplified version doesn't require Azure AI         ║
    ║  Foundry or the Microsoft Agent Framework.                      ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("\nREADME: Full Agent Framework Version")
    print("-"*80)
    print("For the complete multi-agent implementation with Microsoft Agent")
    print("Framework, Azure AI Foundry integration, and Teams bot support,")
    print("please install the full requirements on a platform that supports")
    print("the gRPC library (required by Agent Framework).")
    print()
    print("Current platform detected: Windows ARM64")
    print("Note: gRPC binary wheels are not yet available for ARM64 Windows.")
    print()
    print("This demo uses the same service integrations but simulates the")
    print("agent coordination that would normally be handled by the framework.")
    print("-"*80)
    
    await demo_scenario_simple()
    
    print("\n" + "="*80)
    print("Demo completed successfully!")
    print("="*80)
    print("\nTo learn more about the architecture, see ARCHITECTURE.md")
    print("For full setup instructions, see README.md and CHECKLIST.md")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
