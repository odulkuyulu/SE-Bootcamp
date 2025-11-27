"""
SE Specialist Architecture & Pricing Assistant - Main Demo
Demonstrates the multi-agent workflow for architecture and pricing estimation.
"""

import asyncio
import os
from dotenv import load_dotenv
from agent_framework_azure_ai import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential
from agents.orchestrator import OrchestratorAgent

# Load environment variables
load_dotenv()

# Configuration
FOUNDRY_ENDPOINT = os.getenv("FOUNDRY_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1")


async def demo_scenario_1():
    """Demo Scenario 1: Simple web application requirement."""
    print("\n" + "="*80)
    print("DEMO SCENARIO 1: E-Commerce Web Application")
    print("="*80)
    
    customer_input = """
    We need to build an e-commerce web application for our retail business.
    
    Key requirements:
    - Support for 50,000 active users
    - Product catalog with search and filtering
    - Shopping cart and checkout process
    - User authentication and profiles
    - Order management system
    - Integration with payment gateway
    - Admin dashboard for inventory management
    - Need high availability and performance
    - Budget conscious but willing to invest in reliability
    - Prefer deployment in US East region
    - Must be PCI-DSS compliant for payment processing
    - Need ability to scale for Black Friday traffic (3x normal load)
    """
    
    print(f"\nCustomer Input:\n{customer_input}\n")
    
    async with DefaultAzureCredential() as credential:
        async with AzureAIAgentClient(
            project_endpoint=FOUNDRY_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            async_credential=credential
        ) as chat_client:
            orchestrator = OrchestratorAgent(chat_client)
            results = await orchestrator.process_customer_request(customer_input)
            
            # Print formatted report
            report = orchestrator.format_results(results)
            print(report)
            
            return results


async def demo_scenario_2():
    """Demo Scenario 2: Microservices architecture requirement."""
    print("\n" + "="*80)
    print("DEMO SCENARIO 2: IoT Data Processing Platform")
    print("="*80)
    
    customer_input = """
    We're building an IoT data processing platform for smart building management.
    
    Requirements from the meeting transcript:
    - Collect data from 10,000+ IoT devices (temperature, humidity, occupancy sensors)
    - Real-time data ingestion at 1 million events per hour
    - Stream processing for anomaly detection
    - Historical data storage for analytics (5 years retention)
    - REST API for mobile app integration
    - Machine learning for predictive maintenance
    - Dashboard for building managers
    - Multi-tenant architecture (100 buildings)
    - Need 99.9% uptime SLA
    - Data must stay within US
    - Compliance with GDPR for EU visitors
    - Cost optimization important - variable load (peak during business hours)
    """
    
    print(f"\nCustomer Input:\n{customer_input}\n")
    
    async with DefaultAzureCredential() as credential:
        async with AzureAIAgentClient(
            project_endpoint=FOUNDRY_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            async_credential=credential
        ) as chat_client:
            orchestrator = OrchestratorAgent(chat_client)
            results = await orchestrator.process_customer_request(customer_input)
            
            # Print formatted report
            report = orchestrator.format_results(results)
            print(report)
            
            return results


async def demo_scenario_3():
    """Demo Scenario 3: Simple requirement for quick estimate."""
    print("\n" + "="*80)
    print("DEMO SCENARIO 3: Simple Corporate Website")
    print("="*80)
    
    customer_input = """
    Need a corporate website to replace our outdated on-premises server.
    
    Basic requirements:
    - Company information pages (About, Services, Contact)
    - Blog with 2-3 posts per week
    - Contact form
    - Around 5,000 visitors per month
    - Need SSL certificate
    - Prefer fully managed solution
    - Small IT team, want minimal maintenance
    """
    
    print(f"\nCustomer Input:\n{customer_input}\n")
    
    async with DefaultAzureCredential() as credential:
        async with AzureAIAgentClient(
            project_endpoint=FOUNDRY_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            async_credential=credential
        ) as chat_client:
            orchestrator = OrchestratorAgent(chat_client)
            results = await orchestrator.process_customer_request(customer_input)
            
            # Print formatted report
            report = orchestrator.format_results(results)
            print(report)
            
            return results


async def interactive_mode():
    """Interactive mode for custom input."""
    print("\n" + "="*80)
    print("INTERACTIVE MODE")
    print("="*80)
    print("\nEnter your requirements (press Ctrl+D or Ctrl+Z when done):")
    print("-" * 80)
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    customer_input = "\n".join(lines)
    
    if not customer_input.strip():
        print("No input provided. Exiting interactive mode.")
        return
    
    async with DefaultAzureCredential() as credential:
        async with AzureAIAgentClient(
            project_endpoint=FOUNDRY_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            async_credential=credential
        ) as chat_client:
            orchestrator = OrchestratorAgent(chat_client)
            results = await orchestrator.process_customer_request(customer_input)
            
            # Print formatted report
            report = orchestrator.format_results(results)
            print(report)
            
            return results


async def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("SE SPECIALIST ARCHITECTURE & PRICING ASSISTANT")
    print("Multi-Agent Demo")
    print("="*80)
    
    # Check configuration
    if not FOUNDRY_ENDPOINT:
        print("\n❌ ERROR: FOUNDRY_ENDPOINT not configured!")
        print("Please copy .env.example to .env and configure your Azure AI Foundry settings.")
        return
    
    print("\nConfiguration:")
    print(f"  Endpoint: {FOUNDRY_ENDPOINT}")
    print(f"  Model: {MODEL_DEPLOYMENT_NAME}")
    
    print("\n" + "="*80)
    print("Available Demos:")
    print("  1. E-Commerce Web Application (comprehensive)")
    print("  2. IoT Data Processing Platform (complex microservices)")
    print("  3. Simple Corporate Website (basic)")
    print("  4. Interactive Mode (custom input)")
    print("  0. Exit")
    print("="*80)
    
    while True:
        choice = input("\nSelect demo (0-4): ").strip()
        
        if choice == "0":
            print("\nExiting. Thank you!")
            break
        elif choice == "1":
            await demo_scenario_1()
        elif choice == "2":
            await demo_scenario_2()
        elif choice == "3":
            await demo_scenario_3()
        elif choice == "4":
            await interactive_mode()
        else:
            print("Invalid choice. Please select 0-4.")
        
        print("\n" + "-"*80)
        input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("  1. You've configured .env with your Azure AI Foundry settings")
        print("  2. You're logged in with Azure CLI: az login")
        print("  3. You have the correct permissions and model deployment")
