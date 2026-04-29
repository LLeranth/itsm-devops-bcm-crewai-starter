# src/problem_crew.py
from crewai import Crew, Process
from .agents import ProblemManagementAgents
from .tasks import ProblemManagementTasks

def create_problem_crew(llm): # <--- 1. Accept the llm here
    # 1. Initialize Agents and Tasks
    agents = ProblemManagementAgents()
    tasks = ProblemManagementTasks()

    # 2. Define the specific Agents and assign the local LLM
    classifier = agents.incident_classifier()
    classifier.llm = llm # <--- 2. Force agent to use Ollama
    
    secops = agents.secops_analyst()
    secops.llm = llm
    
    bia = agents.business_impact_analyst()
    bia.llm = llm
    
    recovery = agents.recovery_engineer()
    recovery.llm = llm
    
    change = agents.change_manager()
    change.llm = llm
    
    comms = agents.stakeholder_communicator()
    comms.llm = llm

    # 3. Define the Tasks (no changes needed here)
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