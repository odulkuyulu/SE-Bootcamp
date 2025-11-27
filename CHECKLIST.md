# ✅ Setup Checklist

Use this checklist to get started with the SE Specialist Architecture & Pricing Assistant.

## Prerequisites

### Required
- [ ] Windows 10/11 or Windows Server
- [ ] Python 3.10 or higher installed
- [ ] Azure CLI installed
- [ ] Azure subscription
- [ ] Microsoft Foundry (Azure AI Foundry) project created
- [ ] Model deployed in Microsoft Foundry (gpt-4.1 recommended)

### Optional (for Teams Integration)
- [ ] Microsoft Teams account
- [ ] Azure Bot Service registration
- [ ] Teams Toolkit VS Code extension

## Installation Steps

### 1. Project Setup
- [ ] Clone or download the project
- [ ] Navigate to project directory: `cd "SE Bootcamp"`
- [ ] Review README.md

### 2. Environment Setup
- [ ] Run `.\setup.ps1` (automated) OR follow manual steps:
  - [ ] Create virtual environment: `python -m venv .venv`
  - [ ] Activate: `.\.venv\Scripts\activate`
  - [ ] Upgrade pip: `python -m pip install --upgrade pip`
  - [ ] Install dependencies: `pip install --pre -r requirements.txt`

### 3. Azure Configuration
- [ ] Login to Azure: `az login`
- [ ] Verify account: `az account show`
- [ ] Note your subscription ID
- [ ] Navigate to Azure AI Foundry portal: https://ai.azure.com
- [ ] Create or locate your project
- [ ] Deploy a model (gpt-4.1 or gpt-4.1-mini recommended)
- [ ] Copy the project endpoint (format: https://your-project.cognitiveservices.azure.com/)
- [ ] Copy the model deployment name

### 4. Application Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Edit `.env` with your settings:
  ```
  FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
  MODEL_DEPLOYMENT_NAME=gpt-4.1
  AZURE_SUBSCRIPTION_ID=your-subscription-id
  ```
- [ ] Save the file

### 5. Verification
- [ ] Test Python: `python --version` (should show 3.10+)
- [ ] Test Azure CLI: `az version`
- [ ] Test login: `az account show`
- [ ] Test environment: `.\.venv\Scripts\activate` (should activate)
- [ ] Test imports: `python -c "import agent_framework_azure_ai"`

## Running the Demo

### First Run
- [ ] Ensure virtual environment is activated
- [ ] Run: `python main.py`
- [ ] Verify configuration is loaded
- [ ] See the demo menu

### Demo Scenarios
- [ ] Try Demo 1: E-Commerce Web Application
- [ ] Try Demo 2: IoT Data Processing Platform
- [ ] Try Demo 3: Simple Corporate Website
- [ ] Try Demo 4: Interactive Mode with custom input

### Expected Output
- [ ] See "[Orchestrator] Multi-agent workflow initialized" message
- [ ] See each agent processing in sequence
- [ ] See specification, architecture, and pricing sections
- [ ] See final formatted report

## Troubleshooting

### Common Issues

#### "Import agent_framework could not be resolved"
- [ ] Verified `--pre` flag was used during installation
- [ ] Tried: `pip install --pre --force-reinstall agent-framework-azure-ai`

#### "Authentication failed" or "Unauthorized"
- [ ] Verified Azure CLI login: `az login`
- [ ] Verified correct subscription: `az account show`
- [ ] Verified .env file has correct FOUNDRY_ENDPOINT
- [ ] Checked endpoint format (must include https://)

#### "Model deployment not found"
- [ ] Verified model is deployed in Microsoft Foundry
- [ ] Verified MODEL_DEPLOYMENT_NAME matches exactly
- [ ] Checked model is in "Succeeded" state in portal

#### "No pricing found" warnings
- [ ] This is normal for some services
- [ ] Agent uses estimated pricing as fallback
- [ ] Verify region is correct (eastus, westus, etc.)

#### "Workflow failed" or agent errors
- [ ] Check internet connectivity
- [ ] Verify all environment variables are set
- [ ] Check Azure quotas and limits
- [ ] Review error messages in console

## Advanced Setup

### Custom Model Configuration
- [ ] Edit `.env` to change MODEL_DEPLOYMENT_NAME
- [ ] Options: gpt-4.1, gpt-4.1-mini, gpt-5, etc.
- [ ] Restart application after changes

### Adding New Services
- [ ] Edit `services/ms_learn_service.py`
- [ ] Add service to SERVICE_CATALOG dictionary
- [ ] Include description, SKUs, features
- [ ] Test with demo scenarios

### Customizing Agent Behavior
- [ ] Edit agent files in `agents/` directory
- [ ] Modify instructions in agent initialization
- [ ] Adjust output formats
- [ ] Test thoroughly

### Teams Integration (Advanced)
- [ ] Register bot in Azure Bot Service
- [ ] Configure Teams app manifest
- [ ] Deploy to Azure (App Service or Container Apps)
- [ ] Add to Teams app catalog
- [ ] See `teams/bot.py` for details

## Documentation Reference

- [ ] Read `README.md` for overview
- [ ] Read `DEMO_GUIDE.md` for demo instructions
- [ ] Read `ARCHITECTURE.md` for technical details
- [ ] Read `PROJECT_SUMMARY.md` for comprehensive info

## Performance Tips

### Faster Response Times
- [ ] Use gpt-4.1-mini instead of gpt-4.1 (faster, cheaper)
- [ ] Cache frequently used service information
- [ ] Consider using GitHub Models for free tier

### Cost Optimization
- [ ] Monitor Azure AI Foundry token usage
- [ ] Use appropriate model for task complexity
- [ ] Consider rate limiting for production
- [ ] Implement caching for repeated queries

## Production Deployment Checklist

### Security
- [ ] Use Azure Key Vault for secrets
- [ ] Enable Managed Identity
- [ ] Configure network security groups
- [ ] Implement authentication/authorization
- [ ] Enable audit logging

### Monitoring
- [ ] Configure Application Insights
- [ ] Set up alerts for failures
- [ ] Monitor token usage
- [ ] Track response times
- [ ] Log workflow executions

### Reliability
- [ ] Implement retry logic
- [ ] Add circuit breakers
- [ ] Configure health checks
- [ ] Set up auto-scaling
- [ ] Plan for disaster recovery

## Next Steps

After successful setup:

1. **Explore the Demo**
   - [ ] Run all demo scenarios
   - [ ] Try custom inputs in interactive mode
   - [ ] Review generated reports

2. **Understand the Architecture**
   - [ ] Read through agent code
   - [ ] Trace workflow execution
   - [ ] Study data models

3. **Customize for Your Needs**
   - [ ] Add your own services
   - [ ] Modify agent instructions
   - [ ] Create custom scenarios

4. **Consider Integration**
   - [ ] Plan Teams deployment
   - [ ] Design API endpoints
   - [ ] Consider web interface

5. **Share & Collaborate**
   - [ ] Demo to colleagues
   - [ ] Gather feedback
   - [ ] Iterate on design

## Success Criteria

You've successfully set up the project when:
- ✅ All demo scenarios run without errors
- ✅ Specifications are generated with requirements
- ✅ Architectures include appropriate Azure services
- ✅ Pricing estimates show real costs
- ✅ Final reports are comprehensive and readable

## Support Resources

- **Microsoft Agent Framework**: https://github.com/microsoft/agent-framework
- **Azure AI Foundry**: https://ai.azure.com
- **Azure Pricing API**: https://learn.microsoft.com/rest/api/cost-management/retail-prices
- **Python Documentation**: https://docs.python.org
- **Azure CLI Reference**: https://learn.microsoft.com/cli/azure

## Contact & Feedback

This is a demo project for SE Bootcamp. For questions or improvements:
- Review the documentation in this repository
- Check the GitHub repositories that inspired this project
- Experiment and customize to your needs

---

**Good luck with your demo! 🚀**
