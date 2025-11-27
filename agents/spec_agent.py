"""Spec Agent - Captures customer requirements and asks clarifying questions."""

from agent_framework import ChatAgent, ChatMessage, Executor, WorkflowContext, handler
from models.requirements import SpecificationDocument, CustomerRequirement
from typing_extensions import Never
import json


class SpecAgent(Executor):
    """
    Agent responsible for capturing customer needs and generating a specification document.
    
    This agent:
    1. Analyzes customer input (text or meeting transcripts)
    2. Extracts requirements
    3. Asks clarifying questions
    4. Creates a structured SpecificationDocument
    """
    
    agent: ChatAgent
    
    def __init__(self, chat_client, id: str = "spec_agent"):
        """
        Initialize the Spec Agent.
        
        Args:
            chat_client: Azure AI chat client for creating the agent
            id: Executor ID
        """
        self.agent = chat_client.create_agent(
            instructions="""You are an expert Solution Architect and Requirements Analyst.

Your role is to:
1. Carefully analyze customer input to extract technical and business requirements
2. Ask targeted clarifying questions to fill gaps
3. Identify assumptions and constraints
4. Structure requirements into a clear specification document

When analyzing input:
- Extract functional requirements (what the system should do)
- Extract non-functional requirements (performance, security, scalability)
- Identify technical constraints (budget, timeline, technology preferences)
- Note any ambiguities that need clarification

Your clarifying questions should:
- Be specific and actionable
- Focus on critical architectural decisions
- Help estimate scale and complexity
- Uncover hidden requirements

Output Format:
Return a JSON object with this structure:
{
  "project_title": "Brief project name",
  "summary": "High-level summary of the project",
  "requirements": [
    {
      "requirement_id": "REQ-001",
      "description": "Detailed requirement description",
      "category": "functional|non-functional|technical",
      "priority": "high|medium|low",
      "clarification_needed": true|false
    }
  ],
  "clarifying_questions": ["Question 1?", "Question 2?"],
  "assumptions": ["Assumption 1", "Assumption 2"],
  "constraints": ["Constraint 1", "Constraint 2"],
  "target_users": 10000,
  "target_region": "eastus"
}

Be thorough but concise. Focus on information that impacts architecture and pricing decisions.
""",
            model="gpt-4.1"  # Use a capable reasoning model
        )
        super().__init__(id=id)
    
    @handler
    async def analyze_requirements(
        self,
        customer_input: str,
        ctx: WorkflowContext[Never, SpecificationDocument]
    ) -> None:
        """
        Analyze customer input and generate a specification document.
        
        Args:
            customer_input: Raw customer input (description, transcript, etc.)
            ctx: Workflow context to yield the specification
        """
        # Create the analysis prompt
        prompt = f"""Analyze the following customer input and extract requirements:

Customer Input:
{customer_input}

Generate a comprehensive specification document in the JSON format specified in your instructions.
Focus on extracting actionable requirements and identifying what clarifying questions are needed.
"""
        
        messages = [ChatMessage(role="user", text=prompt)]
        
        try:
            # Run the agent
            response = await self.agent.run(messages)
            response_text = response.text
            
            print(f"\n[SpecAgent] Response from agent:")
            print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
            
            # Parse the JSON response
            # Clean up markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            spec_data = json.loads(response_text.strip())
            
            # Convert to SpecificationDocument
            requirements = [
                CustomerRequirement(**req) for req in spec_data.get("requirements", [])
            ]
            
            spec = SpecificationDocument(
                customer_name=spec_data.get("customer_name"),
                project_title=spec_data.get("project_title", "Untitled Project"),
                summary=spec_data.get("summary", ""),
                requirements=requirements,
                clarifying_questions=spec_data.get("clarifying_questions", []),
                assumptions=spec_data.get("assumptions", []),
                constraints=spec_data.get("constraints", []),
                target_users=spec_data.get("target_users"),
                target_region=spec_data.get("target_region", "eastus")
            )
            
            print(f"\n[SpecAgent] Generated specification with {len(spec.requirements)} requirements")
            print(f"[SpecAgent] Clarifying questions: {len(spec.clarifying_questions)}")
            
            # Yield the specification document to the workflow
            await ctx.yield_output(spec)
            
        except Exception as e:
            print(f"[SpecAgent] Error analyzing requirements: {e}")
            # Create a minimal spec document on error
            error_spec = SpecificationDocument(
                project_title="Error Processing Requirements",
                summary=f"Error occurred: {str(e)}",
                requirements=[],
                clarifying_questions=["Could you provide more details about your requirements?"],
                assumptions=[],
                constraints=[]
            )
            await ctx.yield_output(error_spec)
