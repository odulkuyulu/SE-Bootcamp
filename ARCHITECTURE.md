# Architecture Diagram

## Multi-Agent System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                          USER / SE SPECIALIST                               │
│                                                                             │
│  Input: Customer requirements, meeting transcripts, or descriptions        │
│                                                                             │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        ORCHESTRATOR AGENT                                   │
│                                                                             │
│  • Coordinates workflow                                                     │
│  • Manages data flow                                                        │
│  • Formats final report                                                     │
│                                                                             │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                   ┌──────────────┼──────────────┐
                   │              │              │
                   ▼              ▼              ▼
    ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
    │                  │  │                  │  │                  │
    │   SPEC AGENT     │─▶│   BOM AGENT      │─▶│  PRICING AGENT   │
    │                  │  │                  │  │                  │
    └──────────────────┘  └──────────────────┘  └──────────────────┘
            │                      │                      │
            │                      │                      │
            ▼                      ▼                      ▼
    ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
    │ Specification    │  │ Architecture     │  │ Pricing          │
    │ Document         │  │ Document         │  │ Estimate         │
    │                  │  │                  │  │                  │
    │ • Requirements   │  │ • Services       │  │ • Cost breakdown │
    │ • Questions      │  │ • SKUs           │  │ • Optimizations  │
    │ • Assumptions    │  │ • Architecture   │  │ • Savings        │
    │ • Constraints    │  │ • Security       │  │ • Total cost     │
    └──────────────────┘  └──────────────────┘  └──────────────────┘
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │                              │
                    │      FINAL REPORT            │
                    │                              │
                    │  Ready for SE review and     │
                    │  customer presentation       │
                    │                              │
                    └──────────────────────────────┘
```

## Agent Details

### 1. Spec Agent
**Model**: gpt-4.1  
**Input**: Raw customer input (text, transcript)  
**Processing**:
- Natural language understanding
- Requirement extraction
- Priority assignment
- Gap identification

**Output**: SpecificationDocument
```python
{
  "project_title": str,
  "summary": str,
  "requirements": List[CustomerRequirement],
  "clarifying_questions": List[str],
  "assumptions": List[str],
  "constraints": List[str],
  "target_users": int,
  "target_region": str
}
```

### 2. BOM Agent
**Model**: gpt-4.1  
**Input**: SpecificationDocument  
**Processing**:
- MS Learn service catalog lookup
- Architecture pattern selection
- Service SKU recommendations
- Security and networking design

**Output**: ArchitectureDocument
```python
{
  "project_title": str,
  "architecture_pattern": str,
  "services": List[AzureService],
  "networking": List[str],
  "security": List[str],
  "monitoring": List[str],
  "deployment_notes": List[str],
  "alternatives_considered": List[str]
}
```

### 3. Pricing Agent
**Model**: gpt-4.1  
**Input**: ArchitectureDocument  
**Processing**:
- Azure Retail Prices API queries
- Cost calculations (monthly/annual)
- Savings opportunity identification
- Multi-service cost aggregation

**Output**: PricingEstimate
```python
{
  "project_title": str,
  "region": str,
  "cost_estimates": List[CostEstimate],
  "total_monthly_cost": float,
  "total_annual_cost": float,
  "assumptions": List[str],
  "savings_opportunities": List[str]
}
```

## Integration Points

### External Services

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                   EXTERNAL INTEGRATIONS                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Microsoft Foundry (Azure AI Foundry)                    │
│     • Hosts GPT models                                      │
│     • Project endpoint                                      │
│     • Model deployment                                      │
│                                                             │
│  2. Azure Retail Prices API                                 │
│     • https://prices.azure.com/api/retail/prices            │
│     • No authentication required                            │
│     • Real-time pricing data                                │
│     • OData filtering support                               │
│                                                             │
│  3. MS Learn Knowledge Base                                 │
│     • Azure service catalog (embedded)                      │
│     • Architecture patterns                                 │
│     • Best practices                                        │
│                                                             │
│  4. Azure Identity (DefaultAzureCredential)                 │
│     • Azure CLI login                                       │
│     • Managed Identity                                      │
│     • Service Principal                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Customer Input
    ↓
[Parse & Validate]
    ↓
Spec Agent
    ├─→ Extract requirements
    ├─→ Generate questions
    └─→ Create SpecificationDocument
    ↓
[Pass to BOM Agent]
    ↓
BOM Agent
    ├─→ Query MS Learn service
    ├─→ Design architecture
    ├─→ Select services & SKUs
    └─→ Create ArchitectureDocument
    ↓
[Pass to Pricing Agent]
    ↓
Pricing Agent
    ├─→ Query Azure Pricing API
    ├─→ Calculate costs
    ├─→ Identify savings
    └─→ Create PricingEstimate
    ↓
[Format Report]
    ↓
Final Report
    └─→ Ready for review
```

## Deployment Architecture (Optional)

### Option 1: Azure App Service
```
┌──────────────────────────────────────┐
│     Azure App Service                │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  Python 3.10+ Runtime          │  │
│  │  Multi-Agent Application       │  │
│  │  • Web endpoint                │  │
│  │  • API routes                  │  │
│  │  • Async workers               │  │
│  └────────────────────────────────┘  │
│                                      │
│  Environment Variables:              │
│  • FOUNDRY_ENDPOINT                  │
│  • MODEL_DEPLOYMENT_NAME             │
│  • AZURE_SUBSCRIPTION_ID             │
└──────────────────────────────────────┘
```

### Option 2: Azure Container Apps
```
┌──────────────────────────────────────┐
│  Azure Container Apps                │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  Docker Container              │  │
│  │  • Auto-scaling                │  │
│  │  • HTTPS ingress               │  │
│  │  • Managed identity            │  │
│  └────────────────────────────────┘  │
│                                      │
│  Features:                           │
│  • Scale to zero                     │
│  • Built-in logging                  │
│  • Easy CI/CD                        │
└──────────────────────────────────────┘
```

### Option 3: Microsoft Teams Integration
```
┌────────────────────────────────────────────────┐
│             Microsoft Teams                    │
│                                                │
│  User → Message → Teams Channel                │
│                       ↓                        │
│              Bot Framework                     │
│                       ↓                        │
│           ┌───────────────────────┐            │
│           │   Teams Bot Adapter   │            │
│           └───────────────────────┘            │
│                       ↓                        │
│           ┌───────────────────────┐            │
│           │  Multi-Agent System   │            │
│           │  (deployed on Azure)  │            │
│           └───────────────────────┘            │
│                       ↓                        │
│           ┌───────────────────────┐            │
│           │   Adaptive Card       │            │
│           │   Response            │            │
│           └───────────────────────┘            │
│                       ↓                        │
│              User receives report              │
│                                                │
└────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────┐
│                                                 │
│           APPLICATION LAYER                     │
│                                                 │
│  • Python 3.10+                                 │
│  • AsyncIO for concurrent operations            │
│  • Pydantic for data validation                 │
│  • dotenv for configuration                     │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│           AI/ML LAYER                           │
│                                                 │
│  • Microsoft Agent Framework (preview)          │
│  • agent-framework-azure-ai                     │
│  • Azure AI Foundry integration                 │
│  • GPT-4.1 or GPT-5 models                      │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│           SERVICE LAYER                         │
│                                                 │
│  • httpx for async HTTP                         │
│  • Azure Retail Prices API client              │
│  • MS Learn service catalog                     │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│           SECURITY LAYER                        │
│                                                 │
│  • Azure Identity (DefaultAzureCredential)      │
│  • Azure CLI authentication                     │
│  • Managed Identity support                     │
│  • Environment-based secrets                    │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Scalability & Performance

### Concurrent Processing
- Async/await throughout
- Streaming workflow execution
- Non-blocking API calls
- Parallel service queries

### Error Handling
- Try/catch at agent level
- Fallback pricing estimates
- Graceful degradation
- Comprehensive logging

### Monitoring
- Agent execution logs
- Workflow status events
- Error tracking
- Performance metrics

---

**Note**: This architecture is production-ready and follows Microsoft Agent Framework best practices.
