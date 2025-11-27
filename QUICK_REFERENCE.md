# Quick Reference Card

## 🚀 Quick Start (3 Steps)

```powershell
# 1. Setup
.\setup.ps1

# 2. Configure (edit .env with your Azure AI Foundry settings)
notepad .env

# 3. Run
python main.py
```

## 📋 Essential Commands

```powershell
# Activate virtual environment
.\.venv\Scripts\activate

# Run the demo
python main.py

# Run Teams app (placeholder)
python teams_app.py

# Deactivate virtual environment
deactivate
```

## 🔧 Configuration Quick Reference

Required in `.env`:
```
FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
MODEL_DEPLOYMENT_NAME=gpt-4.1
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

## 📊 Demo Scenarios

| # | Scenario | Use Case | Est. Cost |
|---|----------|----------|-----------|
| 1 | E-Commerce | 50K users, comprehensive | $500-1000/mo |
| 2 | IoT Platform | 10K devices, microservices | $2000-5000/mo |
| 3 | Corporate Site | 5K visitors, simple | $50-200/mo |
| 4 | Interactive | Custom input | Varies |

## 🏗️ Architecture Overview

```
User Input → Orchestrator → Spec Agent → BOM Agent → Pricing Agent → Report
```

## 🤖 The Three Agents

| Agent | Purpose | Output |
|-------|---------|--------|
| **Spec Agent** | Requirements analysis | SpecificationDocument |
| **BOM Agent** | Architecture design | ArchitectureDocument |
| **Pricing Agent** | Cost estimation | PricingEstimate |

## 📁 Project Structure

```
SE Bootcamp/
├── agents/          # Multi-agent implementations
├── models/          # Data models
├── services/        # External service integrations
├── teams/           # Teams bot (placeholder)
├── main.py          # Main demo application
├── setup.ps1        # Automated setup script
└── requirements.txt # Python dependencies
```

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `DEMO_GUIDE.md` | Demo walkthrough |
| `ARCHITECTURE.md` | Technical architecture |
| `PROJECT_SUMMARY.md` | Comprehensive overview |
| `CHECKLIST.md` | Setup checklist |
| `.env.example` | Configuration template |

## 🛠️ Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| Import errors | `pip install --pre --force-reinstall agent-framework-azure-ai` |
| Auth failed | `az login` |
| Model not found | Check MODEL_DEPLOYMENT_NAME in .env |
| No pricing | Normal for some services, uses estimates |

## 💡 Tips & Tricks

### Faster Testing
Use gpt-4.1-mini for faster, cheaper responses:
```env
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

### Better Pricing Accuracy
Use specific regions in requirements:
```
"Deploy in East US (eastus)"
```

### Clearer Requirements
Be specific about:
- User count
- Traffic patterns
- Compliance needs
- Scalability requirements

## 🎯 Expected Output Structure

```
SE SPECIALIST ARCHITECTURE & PRICING REPORT
════════════════════════════════════════════

📋 SPECIFICATION
────────────────────────────────────────────
Project: [Title]
Summary: [Description]
Requirements: [List]
Questions: [List]

🏗️ ARCHITECTURE
────────────────────────────────────────────
Pattern: [Pattern name]
Services: [Azure services with SKUs]
Networking: [Components]
Security: [Measures]

💰 PRICING ESTIMATE
────────────────────────────────────────────
Monthly: $[amount]
Annual: $[amount]
Breakdown: [Per-service costs]
Savings: [Opportunities]
```

## 🌐 Important URLs

- **Azure AI Foundry Portal**: https://ai.azure.com
- **Azure Portal**: https://portal.azure.com
- **Azure Pricing Calculator**: https://azure.microsoft.com/pricing/calculator
- **Azure Retail Prices API**: https://prices.azure.com/api/retail/prices
- **Microsoft Agent Framework**: https://github.com/microsoft/agent-framework

## 📞 Getting Help

1. Check `README.md` for overview
2. Read `DEMO_GUIDE.md` for step-by-step
3. Review `CHECKLIST.md` for setup issues
4. Read `ARCHITECTURE.md` for technical details
5. See `PROJECT_SUMMARY.md` for everything

## 🎓 Learning Path

1. ✅ Run Demo 3 (Simple) - Understand the flow
2. ✅ Run Demo 1 (Comprehensive) - See full capabilities
3. ✅ Try Interactive Mode - Test with your own input
4. ✅ Read agent code - Understand implementation
5. ✅ Customize agents - Make it your own

## 🚀 Deployment Options

| Platform | Best For | Complexity |
|----------|----------|------------|
| Local | Development, demos | Low |
| Azure App Service | Production web app | Medium |
| Azure Container Apps | Scalable containers | Medium |
| Azure Functions | Serverless, event-driven | High |
| Teams Bot | Teams integration | High |

## 💻 VS Code Tips

Recommended extensions:
- Python
- Pylance
- Azure Tools
- Teams Toolkit (for Teams integration)

## 🔐 Security Reminders

- ✅ Never commit `.env` file
- ✅ Use Azure Key Vault in production
- ✅ Enable Managed Identity when deployed
- ✅ Rotate credentials regularly
- ✅ Review Azure RBAC permissions

## 📈 Performance Metrics

Typical execution times (depends on model):
- Spec Agent: 10-30 seconds
- BOM Agent: 15-40 seconds
- Pricing Agent: 20-50 seconds
- **Total**: 45-120 seconds

## 🎨 Customization Ideas

- Add more Azure services to catalog
- Create custom architecture patterns
- Implement cost comparison across regions
- Add export to PowerPoint/PDF
- Build web UI
- Add historical cost tracking

## ✅ Success Indicators

You're ready to demo when:
- All 3 demo scenarios run successfully
- Reports are clear and comprehensive
- Pricing data is realistic
- Clarifying questions are relevant

## 📚 Additional Learning

- **Spec2Cloud**: https://github.com/EmeaAppGbb/spec2cloud
- **Azure Pricing MCP**: https://github.com/charris-msft/azure-pricing-mcp
- **Agent Framework Docs**: https://github.com/microsoft/agent-framework
- **Azure Well-Architected**: https://learn.microsoft.com/azure/well-architected

---

**Keep this card handy during demos! 📌**

Version 1.0 | November 2025
