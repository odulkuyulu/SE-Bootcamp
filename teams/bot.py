"""
Microsoft Teams Bot Integration (Placeholder)

This is a placeholder for Teams integration. Full implementation requires:
1. Teams App registration in Azure AD
2. Bot Framework registration
3. Teams Toolkit configuration
4. Adaptive Card templates

For a complete Teams integration guide, see:
https://learn.microsoft.com/microsoftteams/platform/bots/how-to/create-a-bot-for-teams
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Teams configuration
MICROSOFT_APP_ID = os.getenv("MICROSOFT_APP_ID")
MICROSOFT_APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")
MICROSOFT_APP_TENANT_ID = os.getenv("MICROSOFT_APP_TENANT_ID")


class TeamsBot:
    """
    Placeholder for Teams Bot implementation.
    
    In a full implementation, this would:
    1. Handle Teams message events
    2. Process user queries through the orchestrator
    3. Format responses as Adaptive Cards
    4. Support interactive buttons and forms
    """
    
    def __init__(self, orchestrator):
        """
        Initialize Teams Bot.
        
        Args:
            orchestrator: OrchestratorAgent instance
        """
        self.orchestrator = orchestrator
        print("[TeamsBot] Initialized (placeholder)")
    
    async def on_message_activity(self, turn_context):
        """
        Handle incoming Teams messages.
        
        Args:
            turn_context: Bot Framework turn context
        """
        # Placeholder implementation
        user_message = turn_context.activity.text
        
        # Process through orchestrator
        results = await self.orchestrator.process_customer_request(user_message)
        
        # Format response
        response = self.orchestrator.format_results(results)
        
        # Send back to Teams (in real implementation, use Adaptive Cards)
        await turn_context.send_activity(response)
    
    def create_adaptive_card(self, results: dict) -> dict:
        """
        Create an Adaptive Card for the results.
        
        Args:
            results: Results from orchestrator
        
        Returns:
            Adaptive Card JSON
        """
        spec = results.get("specification")
        arch = results.get("architecture")
        pricing = results.get("pricing")
        
        card = {
            "type": "AdaptiveCard",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Architecture & Pricing Estimate",
                    "weight": "bolder",
                    "size": "large"
                }
            ]
        }
        
        # Add specification section
        if spec:
            card["body"].append({
                "type": "TextBlock",
                "text": f"**Project:** {spec.project_title}",
                "wrap": True
            })
            card["body"].append({
                "type": "TextBlock",
                "text": spec.summary,
                "wrap": True,
                "spacing": "small"
            })
        
        # Add pricing summary
        if pricing:
            card["body"].append({
                "type": "FactSet",
                "facts": [
                    {
                        "title": "Monthly Cost:",
                        "value": f"${pricing.total_monthly_cost:.2f}"
                    },
                    {
                        "title": "Annual Cost:",
                        "value": f"${pricing.total_annual_cost:.2f}"
                    }
                ]
            })
        
        # Add action buttons
        card["actions"] = [
            {
                "type": "Action.OpenUrl",
                "title": "View Full Report",
                "url": "https://portal.azure.com"
            },
            {
                "type": "Action.Submit",
                "title": "Request SE Review",
                "data": {"action": "request_review"}
            }
        ]
        
        return card


# Note: Full Teams integration requires additional setup:
# 1. Create Teams app manifest
# 2. Register bot in Azure Bot Service
# 3. Configure Teams Toolkit
# 4. Deploy to Azure App Service or Container Apps
# 5. Add to Teams app catalog

# Example manifest.json structure:
TEAMS_MANIFEST_TEMPLATE = {
    "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.16/MicrosoftTeams.schema.json",
    "manifestVersion": "1.16",
    "version": "1.0.0",
    "id": "YOUR_APP_ID",
    "packageName": "com.sebootcamp.architecturebot",
    "developer": {
        "name": "SE Bootcamp",
        "websiteUrl": "https://example.com",
        "privacyUrl": "https://example.com/privacy",
        "termsOfUseUrl": "https://example.com/terms"
    },
    "name": {
        "short": "Architecture Assistant",
        "full": "SE Architecture & Pricing Assistant"
    },
    "description": {
        "short": "Get architecture designs and pricing estimates",
        "full": "Multi-agent AI assistant that helps capture requirements, design Azure architectures, and estimate costs."
    },
    "icons": {
        "color": "color.png",
        "outline": "outline.png"
    },
    "accentColor": "#0078D4",
    "bots": [
        {
            "botId": "YOUR_BOT_ID",
            "scopes": ["personal", "team"],
            "supportsFiles": False,
            "isNotificationOnly": False
        }
    ],
    "permissions": ["identity", "messageTeamMembers"],
    "validDomains": ["*.azure.com"]
}
