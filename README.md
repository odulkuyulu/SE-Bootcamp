# SE Specialist Architecture & Pricing Assistant

A multi-agent Teams application that helps Specialists capture customer needs, formulate draft architectures, and generate Azure pricing estimates using AI-powered agents.

## Overview

This solution uses a multi-agent orchestration pattern with specialized agents:

- **Spec Agent**: Captures customer requirements and asks clarifying questions
- **Bill of Materials (BOM) Agent**: Identifies Azure services and components based on requirements
- **Pricing Agent**: Fetches real-time pricing from Azure Retail Prices API
- **Orchestrator Agent**: Routes requests between agents and manages the workflow

## Architecture

```
User Input → Orchestrator Agent
    ├─→ Spec Agent (Requirements Gathering)
    ├─→ BOM Agent (Service Selection & Architecture)
    └─→ Pricing Agent (Cost Estimation)
```

The system leverages:
- **Microsoft Agent Framework** for multi-agent orchestration
- **Microsoft Foundry (Azure AI Foundry)** for model hosting
- **Azure Retail Prices API** for real-time pricing data
- **Microsoft Learn Docs** for Azure service information
- **Microsoft Teams** for user interaction

## Features

- ✅ Capture customer needs from meeting transcripts or direct input
- ✅ Ask clarifying questions to refine requirements
- ✅ Generate draft Azure architecture diagrams
- ✅ Provide detailed pricing estimates
- ✅ Support for multiple Azure regions
- ✅ Export architecture and pricing for SE review

## Prerequisites

- Python 3.10 or higher
- Azure subscription with Microsoft Foundry project
- Microsoft Foundry model deployment (gpt-4.1 or similar)
- Microsoft Teams account (for Teams integration)
- Azure CLI installed

## Quick Start

### 1. Clone and Setup

```powershell
# Navigate to project directory
cd "c:\Users\odulkuyulu\OneDrive - Microsoft\Desktop\SE Bootcamp"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies (--pre flag required for Agent Framework preview)
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```
# Microsoft Foundry Configuration
FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
MODEL_DEPLOYMENT_NAME=your-model-deployment
AZURE_SUBSCRIPTION_ID=your-subscription-id

# Azure Retail Prices API (no auth required)
AZURE_PRICING_API_BASE=https://prices.azure.com/api/retail/prices
```

### 3. Run the Demo

```powershell
# Run the standalone demo
python main.py

# Or run with Teams integration (requires Teams toolkit setup)
python teams_app.py
```

## Project Structure

```
SE Bootcamp/
├── agents/
│   ├── spec_agent.py          # Requirements gathering agent
│   ├── bom_agent.py            # Bill of materials agent
│   ├── pricing_agent.py        # Azure pricing agent
│   └── orchestrator.py         # Main orchestrator
├── services/
│   ├── azure_pricing_service.py    # Azure Retail Prices API client
│   └── ms_learn_service.py         # MS Learn docs integration
├── models/
│   ├── requirements.py         # Data models for requirements
│   ├── architecture.py         # Data models for architecture
│   └── pricing.py              # Data models for pricing
├── teams/
│   ├── bot.py                  # Teams bot integration
│   └── message_handler.py      # Teams message handling
├── main.py                     # Standalone demo entry point
├── teams_app.py                # Teams app entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## Usage Examples

### Example 1: Simple Architecture Request

```python
Input: "I need to build a web application for 10,000 users with a SQL database"

Output:
- Requirements clarification questions
- Recommended architecture (App Service, Azure SQL, etc.)
- Monthly cost estimate with breakdown
```

### Example 2: From Meeting Transcript

```python
Input: [Meeting transcript text]

Output:
- Extracted requirements
- Clarifying questions
- Architecture proposal
- Detailed pricing estimates
```

## Development

### Running Tests

```powershell
pytest tests/
```

### Adding New Agents

1. Create agent class in `agents/` directory
2. Implement the `Executor` pattern with `@handler` methods
3. Register in orchestrator workflow
4. Add tests

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for Azure deployment instructions.

## Contributing

This is a demo project for SE Bootcamp. Contributions and improvements welcome!

## License

MIT License

## Acknowledgments

- Inspired by [spec2cloud](https://github.com/EmeaAppGbb/spec2cloud)
- Azure pricing integration from [azure-pricing-mcp](https://github.com/charris-msft/azure-pricing-mcp)
