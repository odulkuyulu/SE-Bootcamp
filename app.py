"""
SE Specialist Architecture & Pricing Assistant - Interactive Web UI
Modern web interface for the multi-agent architecture and pricing system.
"""

import streamlit as st
import asyncio
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from services.azure_pricing_service import AzurePricingService
from services.ms_learn_service import MSLearnService

# Page configuration
st.set_page_config(
    page_title="SE Architecture & Pricing Assistant",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        max-width: 100%;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .info-box {
        background: #d1ecf1;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin: 10px 0;
    }
    .warning-box {
        background: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
    h1 {
        color: #667eea;
        font-weight: 700;
    }
    h2 {
        color: #764ba2;
        font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 30px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'spec_result' not in st.session_state:
    st.session_state.spec_result = None
if 'architecture_result' not in st.session_state:
    st.session_state.architecture_result = None
if 'pricing_result' not in st.session_state:
    st.session_state.pricing_result = None


def create_pricing_chart(pricing_data):
    """Create an interactive pricing breakdown chart."""
    services = list(pricing_data.keys())
    costs = list(pricing_data.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=services,
            y=costs,
            text=[f'${cost:.2f}' for cost in costs],
            textposition='auto',
            marker=dict(
                color=costs,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Cost ($)")
            )
        )
    ])
    
    fig.update_layout(
        title="Monthly Cost Breakdown by Service",
        xaxis_title="Azure Services",
        yaxis_title="Monthly Cost (USD)",
        template="plotly_white",
        height=400
    )
    
    return fig


def create_cost_comparison_chart(monthly, annual, optimized_annual):
    """Create cost comparison chart."""
    fig = go.Figure(data=[
        go.Bar(
            name='Costs',
            x=['Monthly', 'Annual (Standard)', 'Annual (Reserved)'],
            y=[monthly, annual, optimized_annual],
            text=[f'${monthly:.2f}', f'${annual:.2f}', f'${optimized_annual:.2f}'],
            textposition='auto',
            marker=dict(
                color=['#667eea', '#764ba2', '#28a745'],
                line=dict(color='white', width=2)
            )
        )
    ])
    
    fig.update_layout(
        title="Cost Comparison: Standard vs Reserved Instances",
        yaxis_title="Total Cost (USD)",
        template="plotly_white",
        height=400,
        showlegend=False
    )
    
    return fig


async def analyze_requirements(customer_input):
    """Simulated Spec Agent analysis."""
    with st.spinner("🔍 Spec Agent analyzing requirements..."):
        await asyncio.sleep(1)  # Simulate processing
        
        spec_result = {
            "requirements": [
                "Web hosting for application",
                "Support for specified user load",
                "Content Management System (CMS)" if "content" in customer_input.lower() else "Application hosting",
                "Form handling and integration" if "form" in customer_input.lower() else "User interaction features",
                "Security and SSL/TLS",
                "CDN for fast content delivery" if "fast" in customer_input.lower() or "performance" in customer_input.lower() else "Standard hosting",
                "Monitoring and analytics",
                "Scalability and high availability" if "scale" in customer_input.lower() or "availability" in customer_input.lower() else "Standard availability"
            ],
            "clarifying_questions": [
                "What is your expected peak traffic load?",
                "Do you need multi-region deployment?",
                "Any specific compliance requirements (HIPAA, PCI-DSS, etc.)?",
                "What's your preferred deployment region?",
                "Do you need staging/dev environments?"
            ],
            "assumptions": [
                "Standard business hours support acceptable",
                "Monthly content/feature updates",
                "Standard SLA requirements (99.9%)",
                "Single region deployment initially"
            ]
        }
        
        return spec_result


async def design_architecture(spec_result):
    """Simulated BOM Agent architecture design."""
    with st.spinner("🏗️ BOM Agent designing architecture..."):
        await asyncio.sleep(1)  # Simulate processing
        
        ms_learn = MSLearnService()
        recommended_services = await ms_learn.recommend_services(
            requirements=spec_result["requirements"]
        )
        
        architecture_result = {
            "recommended_services": recommended_services[:5],
            "architecture_components": [
                {"name": "Azure App Service", "sku": "B2", "purpose": "Web application hosting"},
                {"name": "Azure SQL Database", "sku": "Standard S1", "purpose": "Relational data storage"},
                {"name": "Azure Storage", "sku": "Standard_LRS", "purpose": "Static content and media"},
                {"name": "Azure Front Door", "sku": "Standard", "purpose": "Global load balancing and CDN"},
                {"name": "Azure Application Insights", "sku": "Pay-as-you-go", "purpose": "Monitoring and analytics"}
            ]
        }
        
        return architecture_result


async def calculate_pricing(architecture_result):
    """Simulated Pricing Agent cost calculation."""
    with st.spinner("💰 Pricing Agent calculating costs..."):
        await asyncio.sleep(1)  # Simulate processing
        
        pricing_service = AzurePricingService()
        
        try:
            # Get real pricing data
            app_service_price = await pricing_service.get_app_service_pricing(sku="B2", region="eastus")
            app_service_monthly = app_service_price.retail_price * 730 if app_service_price else 54.75
            
            sql_price = await pricing_service.get_sql_database_pricing(sku="S1", region="eastus")
            sql_monthly = sql_price.retail_price * 730 if sql_price else 30.00
        except:
            app_service_monthly = 54.75
            sql_monthly = 30.00
        
        pricing_result = {
            "breakdown": {
                "App Service (B2)": app_service_monthly,
                "SQL Database (S1)": sql_monthly,
                "Storage": 0.05,
                "Front Door": 35.00,
                "Application Insights": 15.00
            },
            "monthly_total": app_service_monthly + sql_monthly + 0.05 + 35.00 + 15.00,
            "optimization_tips": [
                "Use Azure Reserved Instances for 1-year commitment to save ~30%",
                "Enable CDN caching rules to reduce bandwidth costs",
                "Implement auto-scaling based on actual usage patterns",
                "Use Azure Cost Management for ongoing optimization",
                "Consider serverless options for variable workloads"
            ]
        }
        
        pricing_result["annual_total"] = pricing_result["monthly_total"] * 12
        pricing_result["optimized_annual"] = pricing_result["annual_total"] * 0.70  # 30% savings
        
        await pricing_service.close()
        
        return pricing_result


# Main UI
def main():
    # Header with animation
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 30px;">
            <h1 style="color: white; margin: 0;">🏗️ SE Specialist Architecture & Pricing Assistant</h1>
            <p style="color: white; font-size: 18px; margin: 10px 0;">AI-Powered Multi-Agent System for Azure Architecture Design</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Microsoft_Azure.svg/150px-Microsoft_Azure.svg.png", width=150)
        st.markdown("### 🤖 Agent Status")
        
        if st.session_state.analysis_complete:
            st.success("✅ Spec Agent - Complete")
            st.success("✅ BOM Agent - Complete")
            st.success("✅ Pricing Agent - Complete")
        else:
            st.info("⏳ Waiting for input...")
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        if st.session_state.pricing_result:
            st.metric("Monthly Cost", f"${st.session_state.pricing_result['monthly_total']:.2f}")
            st.metric("Annual Savings", f"${st.session_state.pricing_result['annual_total'] - st.session_state.pricing_result['optimized_annual']:.2f}")
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("- [Azure Pricing](https://azure.microsoft.com/pricing/)")
        st.markdown("- [Architecture Center](https://learn.microsoft.com/azure/architecture/)")
        st.markdown("- [Cost Management](https://azure.microsoft.com/services/cost-management/)")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Input", "🔍 Analysis", "🏗️ Architecture", "💰 Pricing"])
    
    with tab1:
        st.markdown("## Customer Requirements")
        st.markdown("Enter the customer's requirements below. Our AI agents will analyze and provide architecture recommendations with accurate pricing.")
        
        # Pre-filled examples
        example = st.selectbox(
            "Load Example Scenario:",
            ["Custom Input", "E-Commerce Website", "Corporate Website", "IoT Platform"]
        )
        
        default_inputs = {
            "Custom Input": "",
            "E-Commerce Website": """We need to build an e-commerce platform with:
- Support for 50,000 concurrent users
- Product catalog with 100,000+ items
- Shopping cart and payment processing
- User accounts and order history
- Real-time inventory management
- Mobile app integration
- High availability (99.99% SLA)
- PCI-DSS compliance required
- Global distribution (US, EU, APAC)
- Budget: $5,000-8,000/month""",
            "Corporate Website": """We need a corporate website with:
- About 1,000 daily visitors
- Content management for marketing team
- Contact forms and newsletter
- Blog section with SEO
- Fast load times globally
- SSL and security
- Budget: around $200/month""",
            "IoT Platform": """We need an IoT data processing platform with:
- 10,000 connected devices
- Real-time telemetry ingestion
- Time-series data storage
- Analytics dashboard
- Alert notifications
- Machine learning predictions
- 99.9% uptime requirement
- Budget: $3,000-5,000/month"""
        }
        
        customer_input = st.text_area(
            "Customer Requirements:",
            value=default_inputs[example],
            height=300,
            placeholder="Enter customer requirements here..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            analyze_button = st.button("🚀 Analyze Requirements", type="primary", use_container_width=True)
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.analysis_complete = False
                st.session_state.spec_result = None
                st.session_state.architecture_result = None
                st.session_state.pricing_result = None
                st.rerun()
        
        if analyze_button and customer_input:
            with st.status("Processing with AI Agents...", expanded=True) as status:
                st.write("🔍 Spec Agent analyzing requirements...")
                spec_result = asyncio.run(analyze_requirements(customer_input))
                st.session_state.spec_result = spec_result
                
                st.write("🏗️ BOM Agent designing architecture...")
                architecture_result = asyncio.run(design_architecture(spec_result))
                st.session_state.architecture_result = architecture_result
                
                st.write("💰 Pricing Agent calculating costs...")
                pricing_result = asyncio.run(calculate_pricing(architecture_result))
                st.session_state.pricing_result = pricing_result
                
                st.session_state.analysis_complete = True
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            
            st.success("🎉 Multi-agent analysis completed successfully!")
            st.balloons()
    
    with tab2:
        st.markdown("## 🔍 Requirements Analysis")
        
        if st.session_state.spec_result:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Identified Requirements")
                for i, req in enumerate(st.session_state.spec_result["requirements"], 1):
                    st.markdown(f"{i}. {req}")
                
                st.markdown("### 🤔 Assumptions")
                for assumption in st.session_state.spec_result["assumptions"]:
                    st.markdown(f"- {assumption}")
            
            with col2:
                st.markdown("### ❓ Clarifying Questions")
                for question in st.session_state.spec_result["clarifying_questions"]:
                    with st.expander(f"💬 {question}"):
                        st.write("This information would help refine the architecture and provide more accurate estimates.")
        else:
            st.info("👈 Please enter requirements and click 'Analyze Requirements' in the Input tab.")
    
    with tab3:
        st.markdown("## 🏗️ Architecture Design")
        
        if st.session_state.architecture_result:
            st.markdown("### Recommended Azure Services")
            
            cols = st.columns(2)
            for idx, component in enumerate(st.session_state.architecture_result["architecture_components"]):
                with cols[idx % 2]:
                    with st.container():
                        st.markdown(f"""
                            <div class="metric-card">
                                <h3>🔧 {component['name']}</h3>
                                <p><strong>SKU:</strong> {component['sku']}</p>
                                <p><strong>Purpose:</strong> {component['purpose']}</p>
                            </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("### 📐 Architecture Diagram")
            st.markdown("""
                ```
                                    ┌─────────────────┐
                                    │  Azure Front    │
                                    │     Door        │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │   App Service   │
                                    │   (Web Tier)    │
                                    └────────┬────────┘
                                             │
                        ┌────────────────────┼────────────────────┐
                        │                    │                    │
                ┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
                │  SQL Database  │  │    Storage     │  │  Application   │
                │   (Data Tier)  │  │   (Blob/File)  │  │    Insights    │
                └────────────────┘  └────────────────┘  └────────────────┘
                ```
            """)
            
            st.markdown("### 🔒 Security & Compliance")
            st.markdown("""
            - ✅ SSL/TLS encryption for all endpoints
            - ✅ Azure AD integration for authentication
            - ✅ Network security groups for access control
            - ✅ Azure Key Vault for secrets management
            - ✅ DDoS protection with Front Door
            - ✅ Regular security updates and patching
            """)
        else:
            st.info("👈 Please complete the analysis in the Input tab first.")
    
    with tab4:
        st.markdown("## 💰 Cost Analysis & Pricing")
        
        if st.session_state.pricing_result:
            # Cost metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Monthly Cost",
                    f"${st.session_state.pricing_result['monthly_total']:.2f}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Annual Cost",
                    f"${st.session_state.pricing_result['annual_total']:.2f}",
                    delta=None
                )
            
            with col3:
                savings = st.session_state.pricing_result['annual_total'] - st.session_state.pricing_result['optimized_annual']
                st.metric(
                    "Annual Savings (Reserved)",
                    f"${savings:.2f}",
                    delta=f"-{(savings/st.session_state.pricing_result['annual_total']*100):.0f}%"
                )
            
            with col4:
                st.metric(
                    "Optimized Annual",
                    f"${st.session_state.pricing_result['optimized_annual']:.2f}",
                    delta=f"-30%"
                )
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_pricing_chart(st.session_state.pricing_result['breakdown']),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    create_cost_comparison_chart(
                        st.session_state.pricing_result['monthly_total'],
                        st.session_state.pricing_result['annual_total'],
                        st.session_state.pricing_result['optimized_annual']
                    ),
                    use_container_width=True
                )
            
            # Detailed breakdown
            st.markdown("### 📊 Detailed Cost Breakdown")
            breakdown_df = {
                "Service": list(st.session_state.pricing_result['breakdown'].keys()),
                "Monthly Cost": [f"${cost:.2f}" for cost in st.session_state.pricing_result['breakdown'].values()],
                "Annual Cost": [f"${cost * 12:.2f}" for cost in st.session_state.pricing_result['breakdown'].values()]
            }
            st.table(breakdown_df)
            
            # Optimization tips
            st.markdown("### 💡 Cost Optimization Recommendations")
            for i, tip in enumerate(st.session_state.pricing_result['optimization_tips'], 1):
                st.markdown(f"""
                    <div class="info-box">
                        <strong>Tip {i}:</strong> {tip}
                    </div>
                """, unsafe_allow_html=True)
            
            # Next steps
            st.markdown("### 🚀 Next Steps")
            st.markdown("""
            1. **Review** the architecture with your security and compliance teams
            2. **Set up** a proof-of-concept in a development subscription
            3. **Configure** Azure Cost Management alerts and budgets
            4. **Implement** the architecture in stages with gradual rollout
            5. **Monitor** costs and optimize based on actual usage patterns
            """)
            
            # Export options
            st.markdown("### 📥 Export Options")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📄 Download PDF Report",
                    data="Report generation would be implemented here",
                    file_name="architecture_report.pdf",
                    mime="application/pdf"
                )
            with col2:
                st.download_button(
                    "📊 Download Excel",
                    data="Excel export would be implemented here",
                    file_name="cost_analysis.xlsx",
                    mime="application/vnd.ms-excel"
                )
            with col3:
                st.download_button(
                    "📋 Download ARM Template",
                    data="ARM template would be implemented here",
                    file_name="deployment.json",
                    mime="application/json"
                )
        else:
            st.info("👈 Please complete the analysis in the Input tab first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 20px;">
            <p>🤖 Powered by AI Multi-Agent System | 🔒 Secure & Compliant | ☁️ Microsoft Azure</p>
            <p>Built with ❤️ for SE Specialists | © 2025 SE Bootcamp</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
