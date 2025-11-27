"""Microsoft Learn documentation service for Azure service information."""

from typing import Optional


class MSLearnService:
    """Service for retrieving Azure service information from MS Learn."""
    
    # Curated Azure service knowledge base
    # In a production system, this would query MS Learn API or use a vector database
    SERVICE_CATALOG = {
        "Azure App Service": {
            "description": "Fully managed platform for building, deploying, and scaling web apps",
            "use_cases": ["Web applications", "REST APIs", "Mobile backends"],
            "skus": ["Free", "Shared", "Basic", "Standard", "Premium", "Isolated"],
            "features": ["Auto-scaling", "Custom domains", "SSL certificates", "Deployment slots"],
            "documentation": "https://learn.microsoft.com/azure/app-service/"
        },
        "Azure SQL Database": {
            "description": "Fully managed relational database with auto-scale, intelligence, and security",
            "use_cases": ["Transactional applications", "Data warehousing", "SaaS applications"],
            "skus": ["Basic", "Standard", "Premium", "General Purpose", "Business Critical", "Hyperscale"],
            "features": ["Automatic backups", "High availability", "Advanced security", "Intelligent performance"],
            "documentation": "https://learn.microsoft.com/azure/azure-sql/database/"
        },
        "Azure Cosmos DB": {
            "description": "Globally distributed, multi-model database service",
            "use_cases": ["IoT", "Gaming", "Retail", "Web and mobile applications"],
            "skus": ["Serverless", "Provisioned throughput", "Autoscale"],
            "features": ["Multi-region replication", "Multiple consistency models", "Low latency"],
            "documentation": "https://learn.microsoft.com/azure/cosmos-db/"
        },
        "Azure Functions": {
            "description": "Serverless compute service for event-driven applications",
            "use_cases": ["Event processing", "Real-time data processing", "Scheduled tasks"],
            "skus": ["Consumption", "Premium", "Dedicated"],
            "features": ["Auto-scaling", "Pay per execution", "Multiple language support"],
            "documentation": "https://learn.microsoft.com/azure/azure-functions/"
        },
        "Azure Kubernetes Service": {
            "description": "Managed Kubernetes container orchestration service",
            "use_cases": ["Microservices", "Container orchestration", "DevOps"],
            "skus": ["Free tier", "Standard", "Premium"],
            "features": ["Auto-scaling", "Integrated CI/CD", "Enterprise-grade security"],
            "documentation": "https://learn.microsoft.com/azure/aks/"
        },
        "Azure Storage": {
            "description": "Scalable cloud storage for data, backups, and archives",
            "use_cases": ["File storage", "Blob storage", "Queue storage", "Table storage"],
            "skus": ["Standard", "Premium"],
            "features": ["High durability", "Geo-replication", "Encryption at rest"],
            "documentation": "https://learn.microsoft.com/azure/storage/"
        },
        "Azure Front Door": {
            "description": "Global load balancer and content delivery network",
            "use_cases": ["Global web applications", "API acceleration", "DDoS protection"],
            "skus": ["Standard", "Premium"],
            "features": ["SSL offloading", "Web Application Firewall", "Smart routing"],
            "documentation": "https://learn.microsoft.com/azure/frontdoor/"
        },
        "Azure Application Insights": {
            "description": "Application Performance Management service",
            "use_cases": ["Application monitoring", "Performance diagnostics", "Usage analytics"],
            "skus": ["Pay-as-you-go"],
            "features": ["Live metrics", "Smart detection", "Distributed tracing"],
            "documentation": "https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview"
        },
        "Azure Virtual Machines": {
            "description": "On-demand scalable computing resources",
            "use_cases": ["Custom applications", "Legacy applications", "Development/testing"],
            "skus": ["A-series", "B-series", "D-series", "E-series", "F-series", "N-series"],
            "features": ["Multiple OS support", "Flexible sizing", "Reserved instances"],
            "documentation": "https://learn.microsoft.com/azure/virtual-machines/"
        },
        "Azure API Management": {
            "description": "Hybrid, multicloud management platform for APIs",
            "use_cases": ["API gateway", "API versioning", "API security"],
            "skus": ["Consumption", "Developer", "Basic", "Standard", "Premium"],
            "features": ["Rate limiting", "Caching", "API analytics", "Developer portal"],
            "documentation": "https://learn.microsoft.com/azure/api-management/"
        }
    }
    
    ARCHITECTURE_PATTERNS = {
        "Web Application": {
            "services": ["Azure App Service", "Azure SQL Database", "Azure Storage", "Azure Application Insights"],
            "description": "Standard web application pattern with managed platform services"
        },
        "Microservices": {
            "services": ["Azure Kubernetes Service", "Azure Cosmos DB", "Azure API Management", "Azure Front Door"],
            "description": "Scalable microservices architecture with container orchestration"
        },
        "Serverless": {
            "services": ["Azure Functions", "Azure Cosmos DB", "Azure Storage", "Azure API Management"],
            "description": "Event-driven serverless architecture for cost optimization"
        },
        "Enterprise Web Application": {
            "services": ["Azure App Service", "Azure SQL Database", "Azure Front Door", "Azure Application Insights"],
            "description": "Enterprise-grade web application with global distribution"
        }
    }
    
    async def get_service_info(self, service_name: str) -> Optional[dict]:
        """Get information about an Azure service."""
        return self.SERVICE_CATALOG.get(service_name)
    
    async def recommend_services(self, requirements: list[str]) -> list[str]:
        """Recommend Azure services based on requirements."""
        recommendations = []
        
        # Simple keyword matching (in production, use semantic search)
        requirement_text = " ".join(requirements).lower()
        
        if any(word in requirement_text for word in ["web", "website", "app", "application"]):
            recommendations.append("Azure App Service")
        
        if any(word in requirement_text for word in ["database", "sql", "data", "storage"]):
            if "nosql" in requirement_text or "document" in requirement_text:
                recommendations.append("Azure Cosmos DB")
            else:
                recommendations.append("Azure SQL Database")
        
        if any(word in requirement_text for word in ["file", "blob", "storage", "backup"]):
            recommendations.append("Azure Storage")
        
        if any(word in requirement_text for word in ["api", "rest", "microservice"]):
            recommendations.append("Azure API Management")
        
        if any(word in requirement_text for word in ["container", "kubernetes", "docker", "microservice"]):
            recommendations.append("Azure Kubernetes Service")
        
        if any(word in requirement_text for word in ["serverless", "function", "event"]):
            recommendations.append("Azure Functions")
        
        if any(word in requirement_text for word in ["global", "cdn", "worldwide", "distribution"]):
            recommendations.append("Azure Front Door")
        
        # Always recommend monitoring
        recommendations.append("Azure Application Insights")
        
        return list(set(recommendations))  # Remove duplicates
    
    async def get_architecture_pattern(self, pattern_name: str) -> Optional[dict]:
        """Get information about an architecture pattern."""
        return self.ARCHITECTURE_PATTERNS.get(pattern_name)
    
    async def suggest_architecture_pattern(self, requirements: list[str]) -> str:
        """Suggest an architecture pattern based on requirements."""
        requirement_text = " ".join(requirements).lower()
        
        if "microservice" in requirement_text or "container" in requirement_text:
            return "Microservices"
        elif "serverless" in requirement_text or "function" in requirement_text:
            return "Serverless"
        elif "enterprise" in requirement_text or "global" in requirement_text:
            return "Enterprise Web Application"
        else:
            return "Web Application"
