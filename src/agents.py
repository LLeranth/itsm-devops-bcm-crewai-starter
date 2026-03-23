from crewai import Agent
from src.tools import get_service_catalog, calculate_impact, failover_service, send_notification

def create_agents():
    detection_agent = Agent(
        role="Vigilant Monitoring Specialist",
        goal="Detect any disruption within 60 seconds and classify severity",
        backstory="You are the always-on eyes of FinServe Digital Bank. You never miss an incident.",
        tools=[get_service_catalog],
        verbose=True,
        allow_delegation=False
    )

    impact_agent = Agent(
        role="Holistic Risk Analyst",
        goal="Calculate exact business impact and recovery priorities using RTO/RPO",
        backstory="You translate technical outages into dollars, customers, and regulatory risk.",
        tools=[calculate_impact],
        verbose=True
    )

    recovery_agent = Agent(
        role="DevOps Recovery Engineer",
        goal="Orchestrate automated failover and restore using DevOps practices",
        backstory="You live by the Three Ways – you automate everything possible.",
        tools=[failover_service],
        verbose=True
    )

    comms_agent = Agent(
        role="Transparent Communicator",
        goal="Keep every stakeholder perfectly informed with clear, calm messages",
        backstory="You embody ITIL 'Collaborate and Promote Visibility' at all times.",
        tools=[send_notification],
        verbose=True
    )

    return [detection_agent, impact_agent, recovery_agent, comms_agent]