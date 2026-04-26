from crewai import Crew, Process
from src.agents import (
    trend_analyst, 
    cmdb_correlator, 
    root_cause_investigator, 
    known_error_author, 
    change_proposer
)
from src.tasks import (
    detection_task, 
    correlation_task, 
    investigation_task, 
    error_authoring_task, 
    change_proposal_task
)

def create_problem_crew():
    return Crew(
        agents=[
            trend_analyst, 
            cmdb_correlator, 
            root_cause_investigator, 
            known_error_author, 
            change_proposer
        ],
        tasks=[
            detection_task, 
            correlation_task, 
            investigation_task, 
            error_authoring_task, 
            change_proposal_task
        ],
        process=Process.sequential, # Required by assignment [cite: 120]
        verbose=True
    )