"""
SE Specialist Architecture & Pricing Assistant - Flask Web UI
Beautiful interactive web interface without heavy dependencies.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import asyncio
import os
from services.azure_pricing_service import AzurePricingService
from services.ms_learn_service import MSLearnService

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for analyzing customer requirements."""
    data = request.json
    customer_input = data.get('customer_input', '')
    
    # Run async analysis
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(perform_analysis(customer_input))
    loop.close()
    
    return jsonify(result)


async def perform_analysis(customer_input):
    """Perform multi-agent analysis."""
    # Step 1: Spec Agent
    spec_result = await analyze_requirements(customer_input)
    
    # Step 2: BOM Agent
    architecture_result = await design_architecture(spec_result)
    
    # Step 3: Pricing Agent
    pricing_result = await calculate_pricing(architecture_result)
    
    return {
        'spec': spec_result,
        'architecture': architecture_result,
        'pricing': pricing_result,
        'success': True
    }


async def analyze_requirements(customer_input):
    """Simulated Spec Agent analysis."""
    await asyncio.sleep(0.5)  # Simulate processing
    
    return {
        "requirements": [
            "Web hosting for application",
            "Support for specified user load",
            "Content Management System" if "content" in customer_input.lower() else "Application hosting",
            "Form handling and integration" if "form" in customer_input.lower() else "User features",
            "Security and SSL/TLS",
            "CDN for fast delivery" if "fast" in customer_input.lower() or "performance" in customer_input.lower() else "Standard hosting",
            "Monitoring and analytics",
            "Scalability" if "scale" in customer_input.lower() else "Standard availability"
        ],
        "clarifying_questions": [
            "What is your expected peak traffic load?",
            "Do you need multi-region deployment?",
            "Any compliance requirements (HIPAA, PCI-DSS)?",
            "Preferred deployment region?",
            "Need staging/dev environments?"
        ],
        "assumptions": [
            "Standard business hours support",
            "Monthly updates",
            "Standard SLA (99.9%)",
            "Single region initially"
        ]
    }


async def design_architecture(spec_result):
    """Simulated BOM Agent architecture design."""
    await asyncio.sleep(0.5)
    
    ms_learn = MSLearnService()
    recommended_services = await ms_learn.recommend_services(
        requirements=spec_result["requirements"]
    )
    
    services_info = []
    for service_name in recommended_services[:5]:
        info = await ms_learn.get_service_info(service_name)
        if info:
            services_info.append({
                "name": service_name,
                "description": info.get('description', ''),
                "use_cases": info.get('use_cases', []),
                "skus": info.get('skus', [])
            })
    
    return {
        "recommended_services": services_info,
        "architecture_components": [
            {"name": "Azure App Service", "sku": "B2", "purpose": "Web application hosting"},
            {"name": "Azure SQL Database", "sku": "Standard S1", "purpose": "Relational data storage"},
            {"name": "Azure Storage", "sku": "Standard_LRS", "purpose": "Static content and media"},
            {"name": "Azure Front Door", "sku": "Standard", "purpose": "Global load balancing"},
            {"name": "Azure Application Insights", "sku": "Pay-as-you-go", "purpose": "Monitoring"}
        ]
    }


async def calculate_pricing(architecture_result):
    """Simulated Pricing Agent cost calculation."""
    await asyncio.sleep(0.5)
    
    pricing_service = AzurePricingService()
    
    try:
        app_service_price = await pricing_service.get_app_service_pricing(sku="B2", region="eastus")
        app_service_monthly = app_service_price.retail_price * 730 if app_service_price else 54.75
        
        sql_price = await pricing_service.get_sql_database_pricing(sku="S1", region="eastus")
        sql_monthly = sql_price.retail_price * 730 if sql_price else 30.00
    except:
        app_service_monthly = 54.75
        sql_monthly = 30.00
    
    breakdown = {
        "App Service (B2)": app_service_monthly,
        "SQL Database (S1)": sql_monthly,
        "Storage": 0.05,
        "Front Door": 35.00,
        "Application Insights": 15.00
    }
    
    monthly_total = sum(breakdown.values())
    annual_total = monthly_total * 12
    optimized_annual = annual_total * 0.70
    
    await pricing_service.close()
    
    return {
        "breakdown": breakdown,
        "monthly_total": round(monthly_total, 2),
        "annual_total": round(annual_total, 2),
        "optimized_annual": round(optimized_annual, 2),
        "savings": round(annual_total - optimized_annual, 2),
        "optimization_tips": [
            "Use Azure Reserved Instances for 1-year commitment to save ~30%",
            "Enable CDN caching rules to reduce bandwidth costs",
            "Implement auto-scaling based on actual usage",
            "Use Azure Cost Management for ongoing optimization",
            "Consider serverless options for variable workloads"
        ]
    }


if __name__ == '__main__':
    # Ensure templates directory exists
    os.makedirs('templates', exist_ok=True)
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║  SE Specialist Architecture & Pricing Assistant                  ║
    ║  Interactive Web UI                                              ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    🚀 Starting web server...
    🌐 Open your browser to: http://localhost:5000
    
    Press CTRL+C to stop the server
    """)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
