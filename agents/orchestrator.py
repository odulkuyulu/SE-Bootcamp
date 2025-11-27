"""Orchestrator Agent - Routes and coordinates between specialized agents."""

from agent_framework import WorkflowBuilder, WorkflowOutputEvent, WorkflowStatusEvent
from agents.spec_agent import SpecAgent
from agents.bom_agent import BOMAgent
from agents.pricing_agent import PricingAgent
from models.requirements import SpecificationDocument
from models.architecture import ArchitectureDocument
from models.pricing import PricingEstimate


class OrchestratorAgent:
    """
    Orchestrator that coordinates the multi-agent workflow.
    
    Workflow:
    1. User Input → SpecAgent → SpecificationDocument
    2. SpecificationDocument → BOMAgent → ArchitectureDocument
    3. ArchitectureDocument → PricingAgent → PricingEstimate
    
    The orchestrator manages the flow and collects the final results.
    """
    
    def __init__(self, chat_client):
        """
        Initialize the orchestrator with all agents.
        
        Args:
            chat_client: Azure AI chat client for creating agents
        """
        self.chat_client = chat_client
        
        # Initialize the three specialized agents
        self.spec_agent = SpecAgent(chat_client)
        self.bom_agent = BOMAgent(chat_client)
        self.pricing_agent = PricingAgent(chat_client)
        
        # Build the workflow
        self.workflow = (
            WorkflowBuilder()
            .set_start_executor(self.spec_agent)
            .add_edge(self.spec_agent, self.bom_agent)
            .add_edge(self.bom_agent, self.pricing_agent)
            .build()
        )
        
        print("[Orchestrator] Multi-agent workflow initialized")
        print("[Orchestrator] Flow: User → Spec Agent → BOM Agent → Pricing Agent")
    
    async def process_customer_request(self, customer_input: str) -> dict:
        """
        Process a customer request through the multi-agent workflow.
        
        Args:
            customer_input: Raw customer input (requirements, meeting transcript, etc.)
        
        Returns:
            Dictionary containing spec, architecture, and pricing
        """
        print(f"\n{'='*80}")
        print("ORCHESTRATOR: Starting Multi-Agent Workflow")
        print(f"{'='*80}\n")
        
        spec_doc = None
        arch_doc = None
        pricing_doc = None
        
        try:
            # Run the workflow with streaming to capture intermediate outputs
            async for event in self.workflow.run_stream(customer_input):
                if isinstance(event, WorkflowStatusEvent):
                    print(f"[Orchestrator] Workflow status: {event.state.value}")
                
                elif isinstance(event, WorkflowOutputEvent):
                    # Capture the output based on type
                    if isinstance(event.data, SpecificationDocument):
                        spec_doc = event.data
                        print(f"\n[Orchestrator] ✓ Specification complete")
                        print(f"  - Project: {spec_doc.project_title}")
                        print(f"  - Requirements: {len(spec_doc.requirements)}")
                        print(f"  - Questions: {len(spec_doc.clarifying_questions)}")
                    
                    elif isinstance(event.data, ArchitectureDocument):
                        arch_doc = event.data
                        print(f"\n[Orchestrator] ✓ Architecture design complete")
                        print(f"  - Pattern: {arch_doc.architecture_pattern}")
                        print(f"  - Services: {len(arch_doc.services)}")
                    
                    elif isinstance(event.data, PricingEstimate):
                        pricing_doc = event.data
                        print(f"\n[Orchestrator] ✓ Pricing estimate complete")
                        print(f"  - Monthly: ${pricing_doc.total_monthly_cost:.2f}")
                        print(f"  - Annual: ${pricing_doc.total_annual_cost:.2f}")
            
            print(f"\n{'='*80}")
            print("ORCHESTRATOR: Workflow Complete")
            print(f"{'='*80}\n")
            
            return {
                "specification": spec_doc,
                "architecture": arch_doc,
                "pricing": pricing_doc,
                "success": True
            }
        
        except Exception as e:
            print(f"\n[Orchestrator] ERROR: {e}")
            return {
                "specification": spec_doc,
                "architecture": arch_doc,
                "pricing": pricing_doc,
                "success": False,
                "error": str(e)
            }
    
    def format_results(self, results: dict) -> str:
        """
        Format the results into a human-readable report.
        
        Args:
            results: Results dictionary from process_customer_request
        
        Returns:
            Formatted report string
        """
        if not results.get("success"):
            return f"ERROR: {results.get('error', 'Unknown error')}"
        
        spec = results.get("specification")
        arch = results.get("architecture")
        pricing = results.get("pricing")
        
        report = []
        report.append("\n" + "="*80)
        report.append("SE SPECIALIST ARCHITECTURE & PRICING REPORT")
        report.append("="*80 + "\n")
        
        # Specification Section
        if spec:
            report.append("📋 SPECIFICATION")
            report.append("-" * 80)
            report.append(f"Project: {spec.project_title}")
            report.append(f"Summary: {spec.summary}\n")
            
            report.append(f"Requirements ({len(spec.requirements)}):")
            for req in spec.requirements[:5]:  # Show first 5
                report.append(f"  [{req.priority.upper()}] {req.description}")
            if len(spec.requirements) > 5:
                report.append(f"  ... and {len(spec.requirements) - 5} more\n")
            
            if spec.clarifying_questions:
                report.append("\nClarifying Questions:")
                for q in spec.clarifying_questions:
                    report.append(f"  • {q}")
            
            report.append("")
        
        # Architecture Section
        if arch:
            report.append("\n🏗️ ARCHITECTURE")
            report.append("-" * 80)
            report.append(f"Pattern: {arch.architecture_pattern}\n")
            
            report.append("Services:")
            for svc in arch.services:
                report.append(f"  • {svc.service_name} ({svc.sku}) x{svc.quantity}")
                report.append(f"    Purpose: {svc.purpose}")
            
            if arch.networking:
                report.append(f"\nNetworking: {', '.join(arch.networking)}")
            if arch.security:
                report.append(f"Security: {', '.join(arch.security)}")
            if arch.monitoring:
                report.append(f"Monitoring: {', '.join(arch.monitoring)}")
            
            report.append("")
        
        # Pricing Section
        if pricing:
            report.append("\n💰 PRICING ESTIMATE")
            report.append("-" * 80)
            report.append(f"Region: {pricing.region}")
            report.append(f"Estimate Date: {pricing.estimate_date.strftime('%Y-%m-%d')}\n")
            
            report.append("Cost Breakdown:")
            for est in pricing.cost_estimates:
                report.append(f"  • {est.service_name} ({est.sku}) x{est.quantity}")
                report.append(f"    Monthly: ${est.monthly_cost:.2f} | Annual: ${est.annual_cost:.2f}")
            
            report.append(f"\n{'─'*80}")
            report.append(f"TOTAL Monthly: ${pricing.total_monthly_cost:.2f}")
            report.append(f"TOTAL Annual:  ${pricing.total_annual_cost:.2f}")
            report.append(f"{'─'*80}\n")
            
            if pricing.savings_opportunities:
                report.append("💡 Cost Optimization Opportunities:")
                for opp in pricing.savings_opportunities:
                    report.append(f"  • {opp}")
            
            report.append("")
        
        report.append("="*80)
        report.append("This report is ready for SE review before presenting to customer.")
        report.append("="*80 + "\n")
        
        return "\n".join(report)
