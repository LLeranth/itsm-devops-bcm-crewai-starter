# src/bia_crew.py
from crewai import Crew, Process
from .agents import ProblemManagementAgents
from .tasks import ProblemManagementTasks

def create_bia_crew():
    # 1. Initialize using the unified classes
    agents = ProblemManagementAgents()
    tasks = ProblemManagementTasks()

    # 2. Assign Agent
    bia_analyst = agents.business_impact_analyst()

    # 3. Create Task Sequence (Using the split BIA tasks)
    t1 = tasks.quantitative_analysis_task(bia_analyst)
    t2 = tasks.compliance_and_vendor_task(bia_analyst, t1)
    t3 = tasks.recovery_prioritization_task(bia_analyst, [t1, t2])

    # 4. Return Crew
    return Crew(
        agents=[bia_analyst],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True
    )