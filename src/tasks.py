from crewai import Task
from src.agents import create_agents

agents = create_agents()

task1 = Task(
    description="Detect the incoming event and classify severity. Event: {event_description}",
    agent=agents[0],
    expected_output="Severity classification and initial incident ticket"
)

task2 = Task(
    description="Perform full business impact assessment with RTO/RPO priorities",
    agent=agents[1],
    expected_output="Prioritized recovery order with exact impact numbers"
)

task3 = Task(
    description="Build and execute the automated recovery plan",
    agent=agents[2],
    expected_output="Step-by-step recovery plan with timestamps"
)

task4 = Task(
    description="Generate and send all stakeholder communications",
    agent=agents[3],
    expected_output="Full set of customer, executive, and regulator messages",
    context=[task1, task2, task3]
)