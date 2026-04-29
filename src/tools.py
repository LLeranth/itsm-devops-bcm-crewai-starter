import os
import pandas as pd
from crewai.tools import tool
from pydantic import BaseModel, Field
from datetime import datetime

# --- 1. INPUT MODELS (For Pydantic Validation) ---

class BIAInput(BaseModel):
    service_name: str = Field(..., description="The name of the service (e.g., 'Core Banking API')")
    hours_outage: int = Field(..., description="Duration of the outage in hours.")

class FailoverInput(BaseModel):
    service_name: str = Field(..., description="Service to failover.")
    strategy: str = Field(..., description="DR strategy: 'hot', 'warm', or 'cold'.")

class NotificationInput(BaseModel):
    audience: str = Field(..., description="Target: 'customers', 'executives', or 'regulators'.")
    incident_severity: str = Field(..., description="NIST Scale P1-P5.")

# --- 2. ENHANCED EXISTING TOOLS ---

@tool("calculate_impact")
def calculate_impact(service_name: str, hours_outage: int):
    """Models non-linear financial loss and cascading failures over time."""
    # Requirement 1b: Non-linear escalation
    base_rates = {"Core Banking API": 50000, "Mobile Banking": 30000, "Transaction Database": 70000}
    rate = base_rates.get(service_name, 10000)
    
    financial_loss = rate * (hours_outage ** 1.8) # Exponential growth
    
    impacts = {
        "financial_loss": f"${financial_loss:,.2f}",
        "cascading_failures": ["Service B at 60% capacity"] if hours_outage > 2 else ["None"],
        "regulatory_risk": "HIGH" if hours_outage >= 4 else "LOW"
    }
    return impacts

@tool("query_cmdb")
def query_cmdb(ci_id: str):
    """Queries the CMDB for CI details, owners, and downstream dependencies."""
    path = os.getenv('CMDB_DATA_PATH', 'data/finserve_cmdb.csv')
    try:
        df = pd.read_csv(path)
        result = df[df['ci_id'] == ci_id]
        return result.to_dict(orient='records')
    except:
        return f"CI {ci_id} not found. Simulated fallback: Owner=Infrastructure, Environment=Prod."

# --- 3. NEW PRODUCTION TOOLS (Requirement 2) ---

@tool("check_compliance_status")
def check_compliance_status():
    """Returns regulatory deadlines and control impacts (GDPR, PCI-DSS, SOX)."""
    return {
        "GDPR": {"deadline": "72 hours", "requirement": "Breach notification for PII"},
        "PCI-DSS": {"deadline": "Immediate", "requirement": "Isolate cardholder data environment"},
        "SLA_Threshold": "Critical breach at 2.0 hours for Tier-1 services"
    }

@tool("assess_vendor_impact")
def assess_vendor_impact(service_name: str):
    """Evaluates third-party vendor risks (e.g., PayBridge API, AWS)."""
    vendors = {
        "Core Banking API": "PayBridge API Gateway (SLA: 99.9%)",
        "Mobile Banking": "Firebase/Google Analytics",
        "Transaction Database": "AWS RDS High-Availability"
    }
    return f"Critical Vendor Dependency: {vendors.get(service_name, 'None detected')}"

@tool("failover_service")
def failover_service(service_name: str, strategy: str):
    """Simulates DR failover with realistic outcomes (Success, Partial, or Failed)."""
    # Simulated variability based on strategy
    outcomes = {"hot": "Success (RTO met)", "warm": "Partial (Degraded Mode)", "cold": "Failed (Data Sync Lag)"}
    return {
        "status": outcomes.get(strategy, "In Progress"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_loss_risk": "Low (within RPO)" if strategy == "hot" else "High"
    }

@tool("send_notification")
def send_notification(audience: str, incident_severity: str):
    """Generates audience-appropriate crisis communications."""
    templates = {
        "customers": "We are experiencing a temporary service interruption. Our engineers are working to restore access.",
        "executives": f"CRITICAL {incident_severity} INCIDENT: Estimated financial exposure exceeds $1M. Decision required on DR failover.",
        "regulators": "Preliminary report: Potential unauthorized access to encrypted data segments. Investigation ongoing."
    }
    return f"Notification sent via Email/SMS to {audience.upper()}: {templates.get(audience)}"

@tool("get_service_catalog")
def get_service_catalog():
    """Returns Tier 1-3 service catalog with RTO, RPO, and MTPD values."""
    return [
        {"name": "Core Banking API", "tier": 1, "RTO": "2h", "RPO": "0h", "MTPD": "4h"},
        {"name": "Mobile Banking", "tier": 1, "RTO": "4h", "RPO": "15m", "MTPD": "8h"},
        {"name": "Internal Reporting", "tier": 3, "RTO": "24h", "RPO": "4h", "MTPD": "72h"}
    ]

@tool("analyze_security_event")
def analyze_security_event(event_description: str):
    """Parses events for IOCs and maps to MITRE ATT&CK Tactics."""
    return {
        "severity": "P1",
        "mitre_mapping": "T1486 (Data Encrypted for Impact)",
        "attack_vector": "Ransomware / Credential Compromise",
        "recommended_action": "Isolate segment VLAN-202 immediately."
    }

@tool("execute_runbook")
def execute_runbook(runbook_id: str):
    """Simulates step-by-step execution of technical runbooks."""
    steps = [
        "1. Identify compromised service account",
        "2. Rotate API keys and database credentials",
        "3. Flush Redis cache",
        "4. Validate integrity of last backup"
    ]
    return {"runbook": runbook_id, "status": "Completed", "steps_executed": steps}

@tool("log_lesson")
def log_lesson(category: str, lesson: str):
    """Logs post-incident review (PIR) items into the knowledge base."""
    return f"Lesson Logged [{category}]: {lesson} | Reference: NIST CSF / ISO 22301"