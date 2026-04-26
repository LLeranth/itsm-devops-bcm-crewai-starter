from crewai import Task
from src.agents import (
    trend_analyst, 
    cmdb_correlator, 
    root_cause_investigator, 
    known_error_author, 
    change_proposer
)

# 1. Problem Detection (Stage 1)
detection_task = Task(
    description="Analyze the incident CSV data to recognize shared causes and clusters using trend analysis. Group by service, error codes, and time windows[cite: 40, 41, 129].",
    agent=trend_analyst,
    expected_output="Candidate pattern clusters with statistical summaries (counts, frequencies)[cite: 73, 136]."
)

# 2. Problem Logging & Classification (Stage 2)
correlation_task = Task(
    description="Enrich detected patterns by querying the CMDB and change logs. Link incidents to specific Configuration Items (CIs) and recent deployments[cite: 45, 50, 73].",
    agent=cmdb_correlator,
    expected_output="Enriched patterns including CI data, dependency mappings, and related change IDs[cite: 73].",
    context=[detection_task] # Context chaining [cite: 76, 145]
)

# 3. Root Cause Analysis (Stage 3)
investigation_task = Task(
    description="Perform a structured 'Five Whys' analysis for each pattern to determine the underlying cause. Cross-reference the CMDB and change logs[cite: 48, 49, 158].",
    agent=root_cause_investigator,
    expected_output="Specific, causal root cause determination for each pattern supported by evidence[cite: 73, 137].",
    context=[detection_task, correlation_task]
)

# 4. Known Error Documentation (Stage 4)
error_authoring_task = Task(
    description="Document the root cause and provide a clear workaround for the Service Desk. Create a formal Known Error record[cite: 58, 59, 62].",
    agent=known_error_author,
    expected_output="Well-formed Known Error records (JSON/Markdown) including root_cause, workaround, and permanent_fix[cite: 125, 150].",
    context=[investigation_task]
)

# 5. Resolution via Change (Stage 5)
change_proposal_task = Task(
    description="Generate a formal Request for Change (RFC) for a permanent fix. Include risk ratings, testing requirements, and a rollback plan[cite: 63, 64, 132].",
    agent=change_proposer,
    expected_output="RFC documents including risk ratings, implementation plans, and scheduling[cite: 73, 139].",
    context=[investigation_task, error_authoring_task]
)