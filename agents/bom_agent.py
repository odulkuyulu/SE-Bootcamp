"""BOM Agent - Generates Bill of Materials and Architecture Design."""

from agent_framework import ChatAgent, ChatMessage, Executor, WorkflowContext, handler
from models.requirements import SpecificationDocument
from models.architecture import ArchitectureDocument, AzureService
from services.ms_learn_service import MSLearnService
import json


class BOMAgent(Executor):
    """
    Agent responsible for creating the Bill of Materials and architecture design.
    
    This agent:
    1. Analyzes requirements from SpecificationDocument
    2. Selects appropriate Azure services using MS Learn knowledge
    3. Designs the architecture pattern
    4. Creates a detailed ArchitectureDocument
    """
    
    agent: ChatAgent
    ms_learn: MSLearnService
    
    def __init__(self, chat_client, id: str = "bom_agent"):
        """
        Initialize the BOM Agent.
        
        Args:
            chat_client: Azure AI chat client for creating the agent
            id: Executor ID
        """
        self.ms_learn = MSLearnService()
        
        self.agent = chat_client.create_agent(
            instructions="""You are an expert Azure Solutions Architect with deep knowledge of Azure services.

Your role is to:
1. Analyze customer requirements and design appropriate Azure architectures
2. Select the right Azure services based on requirements
3. Recommend appropriate SKUs and tiers
4. Create a comprehensive Bill of Materials (BOM)
5. Consider cost optimization, scalability, security, and best practices

When designing architectures:
- Choose services that best fit the requirements
- Consider scalability and growth
- Recommend appropriate redundancy and availability
- Include networking, security, and monitoring components
- Think about DevOps and deployment strategies

Output Format:
Return a JSON object with this structure:
{
  "project_title": "Project name from spec",
  "architecture_pattern": "Pattern name (e.g., Web Application, Microservices)",
  "services": [
    {
      "service_name": "Azure App Service",
      "sku": "Standard_S1",
      "quantity": 2,
      "region": "eastus",
      "purpose": "Host web application with auto-scaling",
      "dependencies": ["Azure SQL Database", "Azure Storage"]
    }
  ],
  "networking": ["Virtual Network", "Application Gateway"],
  "security": ["Azure Key Vault", "Managed Identity", "Azure AD"],
  "monitoring": ["Azure Monitor", "Application Insights", "Log Analytics"],
  "deployment_notes": ["Use CI/CD with Azure DevOps", "Infrastructure as Code with Bicep"],
  "alternatives_considered": ["Alternative 1", "Alternative 2"]
}

Be specific about SKU recommendations. Consider cost-effectiveness while meeting requirements.
""",
            model="gpt-4.1"
        )
        super().__init__(id=id)
    
    @handler
    async def design_architecture(
        self,
        spec: SpecificationDocument,
        ctx: WorkflowContext[ArchitectureDocument]
    ) -> None:
        """
        Design architecture based on the specification document.
        
        Args:
            spec: SpecificationDocument from SpecAgent
            ctx: Workflow context to send the architecture
        """
        try:
            # Get service recommendations from MS Learn
            requirement_texts = [req.description for req in spec.requirements]
            recommended_services = await self.ms_learn.recommend_services(requirement_texts)
            suggested_pattern = await self.ms_learn.suggest_architecture_pattern(requirement_texts)
            
            print(f"\n[BOMAgent] Recommended services: {', '.join(recommended_services)}")
            print(f"[BOMAgent] Suggested pattern: {suggested_pattern}")
            
            # Build the prompt with context
            service_info = []
            for service_name in recommended_services:
                info = await self.ms_learn.get_service_info(service_name)
                if info:
                    service_info.append(f"- {service_name}: {info['description']}, SKUs: {', '.join(info['skus'])}")
            
            prompt = f"""Design an Azure architecture for the following project:

Project: {spec.project_title}
Summary: {spec.summary}

Requirements:
{chr(10).join([f"- [{req.priority.upper()}] {req.description}" for req in spec.requirements])}

Target Users: {spec.target_users or 'Not specified'}
Target Region: {spec.target_region}

Constraints:
{chr(10).join([f"- {c}" for c in spec.constraints]) if spec.constraints else "None specified"}

Recommended Azure Services:
{chr(10).join(service_info)}

Suggested Architecture Pattern: {suggested_pattern}

Design a comprehensive architecture with appropriate Azure services, SKUs, and configurations.
Generate the architecture document in the JSON format specified in your instructions.
"""
            
            messages = [ChatMessage(role="user", text=prompt)]
            
            # Run the agent
            response = await self.agent.run(messages)
            response_text = response.text
            
            print(f"\n[BOMAgent] Response from agent:")
            print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
            
            # Parse the JSON response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            arch_data = json.loads(response_text.strip())
            
            # Convert to ArchitectureDocument
            services = [
                AzureService(**svc) for svc in arch_data.get("services", [])
            ]
            
            architecture = ArchitectureDocument(
                project_title=arch_data.get("project_title", spec.project_title),
                architecture_pattern=arch_data.get("architecture_pattern", suggested_pattern),
                services=services,
                networking=arch_data.get("networking", []),
                security=arch_data.get("security", []),
                monitoring=arch_data.get("monitoring", []),
                deployment_notes=arch_data.get("deployment_notes", []),
                alternatives_considered=arch_data.get("alternatives_considered", [])
            )
            
            print(f"\n[BOMAgent] Generated architecture with {len(architecture.services)} services")
            print(f"[BOMAgent] Pattern: {architecture.architecture_pattern}")
            
            # Send the architecture document to the next agent
            await ctx.send_message(architecture)
            
        except Exception as e:
            print(f"[BOMAgent] Error designing architecture: {e}")
            # Create a minimal architecture on error
            error_arch = ArchitectureDocument(
                project_title=spec.project_title,
                architecture_pattern="Error",
                services=[],
                networking=[],
                security=[],
                monitoring=[],
                deployment_notes=[f"Error occurred: {str(e)}"],
                alternatives_considered=[]
            )
            await ctx.send_message(error_arch)
