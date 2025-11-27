"""
Microsoft Teams App Entry Point (Placeholder)

This is a placeholder for the Teams app server.
Full implementation requires Azure Bot Service setup.
"""

import os
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", 3978))


async def messages_handler(req):
    """Handle incoming Teams messages."""
    # Placeholder implementation
    # In production, this would:
    # 1. Validate Bot Framework tokens
    # 2. Parse incoming activities
    # 3. Route to TeamsBot handler
    # 4. Return responses
    
    return web.Response(text="Teams bot placeholder", status=200)


def create_app():
    """Create the aiohttp web application."""
    app = web.Application()
    app.router.add_post("/api/messages", messages_handler)
    return app


if __name__ == "__main__":
    print(f"""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║            TEAMS INTEGRATION PLACEHOLDER                           ║
║                                                                    ║
║  This is a placeholder for Microsoft Teams integration.           ║
║                                                                    ║
║  To implement full Teams integration:                             ║
║                                                                    ║
║  1. Register your bot in Azure Bot Service                        ║
║     https://portal.azure.com → Bot Services                       ║
║                                                                    ║
║  2. Configure authentication:                                     ║
║     - MICROSOFT_APP_ID                                            ║
║     - MICROSOFT_APP_PASSWORD                                      ║
║     - MICROSOFT_APP_TENANT_ID                                     ║
║                                                                    ║
║  3. Install Teams Toolkit extension in VS Code                    ║
║                                                                    ║
║  4. Create Teams app manifest (see teams/bot.py)                  ║
║                                                                    ║
║  5. Deploy to Azure:                                              ║
║     - Azure App Service                                           ║
║     - Azure Container Apps                                        ║
║     - Azure Functions                                             ║
║                                                                    ║
║  6. Test in Teams client or Teams Toolkit                         ║
║                                                                    ║
║  Resources:                                                        ║
║  - Bot Framework: https://dev.botframework.com/                   ║
║  - Teams Toolkit: https://aka.ms/teams-toolkit                    ║
║  - Teams Docs: https://learn.microsoft.com/microsoftteams         ║
║                                                                    ║
║  For now, use main.py for the standalone demo.                    ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"\nPlaceholder server would run on port {PORT}")
    print("Run 'python main.py' instead for the demo.\n")


# Uncomment to run the placeholder server:
# if __name__ == "__main__":
#     app = create_app()
#     web.run_app(app, port=PORT)
