# SE Specialist Architecture & Pricing Assistant - Demo Guide

## Overview

This demo showcases a multi-agent AI system that helps SE Specialists capture customer requirements, design Azure architectures, and generate pricing estimates.

## Quick Start

### 1. Prerequisites Check

```powershell
# Verify Python version (3.10+)
python --version

# Verify Azure CLI login
az account show

# Verify you have a Microsoft Foundry project with a model deployed
```

### 2. Installation

```powershell
# Navigate to project
cd "c:\Users\odulkuyulu\OneDrive - Microsoft\Desktop\SE Bootcamp"

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies (--pre flag is REQUIRED for Agent Framework preview)
pip install --pre -r requirements.txt
```

### 3. Configuration

```powershell
# Copy the environment template
copy .env.example .env

# Edit .env with your settings
notepad .env
```

Required configuration in `.env`:

```
# Get these from Azure AI Foundry portal
FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
MODEL_DEPLOYMENT_NAME=gpt-4.1

# Your Azure subscription
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

### 4. Run the Demo

```powershell
python main.py
```

## Demo Scenarios

### Scenario 1: E-Commerce Web Application
**Purpose**: Demonstrates comprehensive requirement analysis with security and scalability considerations.

**Input**: Detailed requirements for a 50,000-user e-commerce platform with PCI compliance needs.

**Expected Output**:
- Requirements specification with priorities
- Architecture using App Service, SQL Database, Storage
- Monthly cost estimate around $500-1000
- Cost optimization recommendations

### Scenario 2: IoT Data Processing Platform
**Purpose**: Shows handling of complex microservices architecture with real-time processing.

**Input**: Requirements for IoT platform with 10,000+ devices and real-time analytics.

**Expected Output**:
- Multi-tier architecture with IoT Hub, Functions, Cosmos DB
- Event-driven architecture pattern
- Higher cost estimate ($2000-5000/month)
- Scaling and performance recommendations

### Scenario 3: Simple Corporate Website
**Purpose**: Demonstrates quick estimates for simple requirements.

**Input**: Basic corporate website with minimal traffic.

**Expected Output**:
- Simple architecture with App Service + Storage
- Low cost estimate ($50-200/month)
- Managed service recommendations

### Scenario 4: Interactive Mode
**Purpose**: Allows you to test with custom requirements.

**Usage**: Paste your own requirements or meeting transcript, then press Ctrl+Z (Windows) or Ctrl+D (Linux/Mac).

## Understanding the Output

### 1. Specification Section (📋)
- **Project Title**: Auto-generated project name
- **Summary**: High-level description
- **Requirements**: Categorized and prioritized requirements
- **Clarifying Questions**: Questions for the SE to ask the customer

### 2. Architecture Section (🏗️)
- **Pattern**: Chosen architecture pattern (Web App, Microservices, etc.)
- **Services**: List of Azure services with SKUs and purposes
- **Networking**: Network components (VNet, Gateway, etc.)
- **Security**: Security measures (Key Vault, Managed Identity)
- **Monitoring**: Observability components

### 3. Pricing Section (💰)
- **Cost Breakdown**: Per-service monthly and annual costs
- **Total Costs**: Aggregated monthly and annual estimates
- **Assumptions**: Pricing assumptions (24/7 operation, etc.)
- **Savings Opportunities**: Reserved instances, spot VMs, etc.

## Multi-Agent Architecture

The solution uses Microsoft Agent Framework with this workflow:

```
User Input
    ↓
Orchestrator Agent
    ↓
Spec Agent (Requirements Analysis)
    ↓
BOM Agent (Architecture Design)
    ↓
Pricing Agent (Cost Estimation)
    ↓
Final Report
```

### Agent Responsibilities

1. **Spec Agent** (`spec_agent.py`)
   - Analyzes customer input
   - Extracts requirements
   - Generates clarifying questions
   - Output: SpecificationDocument

2. **BOM Agent** (`bom_agent.py`)
   - Designs architecture
   - Selects Azure services
   - Recommends SKUs
   - Output: ArchitectureDocument

3. **Pricing Agent** (`pricing_agent.py`)
   - Fetches real-time pricing from Azure API
   - Calculates cost estimates
   - Provides optimization recommendations
   - Output: PricingEstimate

4. **Orchestrator** (`orchestrator.py`)
   - Coordinates agent workflow
   - Manages data flow
   - Formats final report

## Customization Tips

### Changing the AI Model

Edit `.env`:
```
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini  # Faster, cheaper
# or
MODEL_DEPLOYMENT_NAME=gpt-5  # More advanced
```

### Adding Custom Services

Edit `services/ms_learn_service.py`:
```python
SERVICE_CATALOG = {
    "Your Custom Service": {
        "description": "...",
        "use_cases": ["..."],
        # ...
    }
}
```

### Modifying Agent Instructions

Edit the agent files (e.g., `agents/spec_agent.py`):
```python
self.agent = chat_client.create_agent(
    instructions="Your custom instructions here..."
)
```

## Troubleshooting

### "Import agent_framework could not be resolved"
**Solution**: Install with `--pre` flag:
```powershell
pip install --pre agent-framework-azure-ai
```

### "Authentication failed"
**Solution**: Ensure you're logged in:
```powershell
az login
az account show
```

### "Model deployment not found"
**Solution**: Verify your model deployment name in Azure AI Foundry portal matches your `.env` file.

### Pricing API returns no results
**Issue**: Azure Pricing API may not have data for all SKUs.
**Solution**: The agent uses estimated pricing as fallback.

## Next Steps

### Integration with Microsoft Teams
See `teams_app.py` for Teams bot integration (requires Teams App setup).

### Deployment to Azure
Deploy the multi-agent system as an Azure Function or Container App for production use.

### Adding More Agents
1. Create new agent in `agents/` directory
2. Implement the `Executor` pattern
3. Add to orchestrator workflow
4. Test with demo scenarios

## Demo Presentation Tips

1. **Start with Scenario 3** (simple website) - Quick win to show the flow
2. **Move to Scenario 1** (e-commerce) - Shows comprehensive analysis
3. **Show Interactive Mode** - Demonstrates flexibility
4. **Discuss the Architecture** - Explain the multi-agent pattern
5. **Highlight Key Features**:
   - Real-time Azure pricing
   - Intelligent requirements analysis
   - Cost optimization recommendations
   - Production-ready patterns

## Additional Resources

- **Microsoft Agent Framework**: https://github.com/microsoft/agent-framework
- **Azure Pricing API**: https://learn.microsoft.com/rest/api/cost-management/retail-prices/azure-retail-prices
- **Azure AI Foundry**: https://ai.azure.com
- **Spec2Cloud** (inspiration): https://github.com/EmeaAppGbb/spec2cloud

## Support

For issues or questions about this demo, refer to:
- README.md - Main documentation
- requirements.txt - Dependencies
- .env.example - Configuration template
