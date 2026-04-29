# src/tasks.py
from crewai import Task
from pydantic import BaseModel
from typing import List, Dict

# --- Pydantic Models for Structured Output (Speeds up weak CPUs) ---

class ImpactData(BaseModel):
    service_name: str
    financial_loss_projection: Dict[str, str]
    escalation_point_hours: int

class ContainmentReport(BaseModel):
    isolated_systems: List[str]
    mitre_tactics: List[str]
    forensic_status: str

# --- Task Definitions ---

class ProblemManagementTasks:
    
    def triage_task(self, agent):
        return Task(
            description="""Analyze the initial security event and monitoring data. 
            Identify the affected service, determine the NIST severity level (P1-P5), 
            and query the CMDB to find downstream dependencies.""",
            expected_output="A triage report with severity rating and a list of impacted CIs.",
            agent=agent
        )

    def containment_task(self, agent, context_task):
        return Task(
            description="""Using the triage report, execute the appropriate security runbooks 
            to isolate the affected network segments. Identify the MITRE ATT&CK tactic 
            used and ensure forensic evidence (snapshots) is preserved before any recovery.""",
            expected_output="A containment summary confirming isolation of affected systems.",
            output_json=ContainmentReport,
            agent=agent,
            context=[context_task]
        )

    def quantitative_analysis_task(self, agent, context_task):
        return Task(
            description="""Calculate the non-linear financial impact for the affected service.
            Execute the 'calculate_impact' tool for 1, 2, and 4 hour intervals. 
            Identify the 'Financial Escalation Point' where costs spike due to SLAs.""",
            expected_output="A BIA summary showing cost escalation and regulatory risks.",
            output_json=ImpactData,
            agent=agent,
            context=[context_task]
        )

    def recovery_task(self, agent, context_tasks):
        return Task(
            description="""Based on the BIA and containment status, execute the failover_service 
            tool. Validate that the DR site is synchronized and services meet minimum 
            viable operation levels. Report any replication lag or RPO violations.""",
            expected_output="A technical recovery log showing failover results and stability checks.",
            agent=agent,
            context=context_tasks
        )

    def emergency_change_task(self, agent, context_task):
        return Task(
            description="""Review the recovery actions for compliance. Document the 
            emergency change (RFC) including risk assessment and rollback plans. 
            Ensure all manual interventions are logged for the Emergency CAB.""",
            expected_output="A formal Emergency RFC Markdown file saved to the output folder.",
            agent=agent,
            context=[context_task]
        )

    def communication_task(self, agent, context_tasks):
        return Task(
            description="""Synthesize all incident data to create audience-specific notifications.
            Generate messages for Customers (empathetic), Executives (financial), 
            and Regulators (compliance-focused). Ensure GDPR/PCI-DSS deadlines are met.""",
            expected_output="A set of four finalized notifications sent via the notification tool.",
            agent=agent,
            context=context_tasks
        )

    def compliance_and_vendor_task(self, agent, context_task):
        return Task(
            description="""Based on the financial impact results, identify specific 
            regulatory notification deadlines (GDPR/PCI-DSS). Use the assess_vendor_impact 
            tool to check if third-party providers are breaching their SLAs.""",
            expected_output="A report detailing legal deadlines and vendor SLA risks.",
            agent=agent,
            context=[context_task]
        )

    def recovery_prioritization_task(self, agent, context_list):
        return Task(
            description="""Synthesize quantitative financial data and qualitative compliance 
            requirements. Produce a prioritized recovery sequence (1st, 2nd, 3rd) 
            justifying why certain services must be restored before others based on MTPD.""",
            expected_output="A formal BIA summary report with a prioritized recovery roadmap.",
            agent=agent,
            context=context_list
        )

    def detection_task(self, agent):
        """Standard ITIL detection for the Trend Analyst role."""
        return Task(
            description="""Analyze incident logs for clusters. Look for recurring 
            error codes and temporal spikes to identify an underlying Problem.""",
            expected_output="A list of 3-4 identified incident clusters.",
            agent=agent
        )