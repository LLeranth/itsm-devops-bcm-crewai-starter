# src/problem_crew.py
from crewai import Crew, Process
from .agents import ProblemManagementAgents
from .tasks import ProblemManagementTasks

def create_problem_crew():
    # 1. Initialize Agents and Tasks
    agents = ProblemManagementAgents()
    tasks = ProblemManagementTasks()

    # 2. Define the specific Agents (Updated to match our new agents.py)
    classifier = agents.incident_classifier()
    secops     = agents.secops_analyst()
    bia        = agents.business_impact_analyst()
    recovery   = agents.recovery_engineer()
    change     = agents.change_manager()
    comms      = agents.stakeholder_communicator()

    # 3. Define the Tasks and their sequence (Updated to match our new tasks.py)
    t1 = tasks.triage_task(classifier)
    t2 = tasks.containment_task(secops, t1)
    t3 = tasks.quantitative_analysis_task(bia, t2)
    t4 = tasks.recovery_task(recovery, [t2, t3])
    t5 = tasks.emergency_change_task(change, t4)
    t6 = tasks.communication_task(comms, [t3, t5])

    # 4. Create the Crew
    return Crew(
        agents=[classifier, secops, bia, recovery, change, comms],
        tasks=[t1, t2, t3, t4, t5, t6],
        process=Process.sequential, 
        verbose=True
    )