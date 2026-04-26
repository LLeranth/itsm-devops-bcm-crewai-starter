import os
from dotenv import load_dotenv
from crewai import Agent, LLM

# Load environment variables (API_BASE, MODEL_NAME, etc.)
load_dotenv()

# 1. Configure the Local LLM (Llama 3.1 8B via Ollama)
# The 'ollama/' prefix is MANDATORY to avoid OpenAI 401 errors.
problem_llm = LLM(
    model=os.getenv('OPENAI_MODEL_NAME', 'ollama/llama3.1:8b'),
    base_url=os.getenv('OPENAI_API_BASE', 'http://localhost:11434/v1'),
    api_key='NA',
    timeout=1200 # Required for complex CSV analysis
)

# 2. Define the Agents

# STAGE 1: Problem Detection
trend_analyst = Agent(
    role="Trend Analyst",
    goal="Identify recurring incident patterns using statistical evidence from incident logs.",
    backstory="""You are a senior analyst at FinServe Digital Bank. You specialize in 
    identifying recurring incident patterns by analyzing service, error code, 
    subcategory, and temporal clustering. You always provide statistical evidence 
    (counts/frequencies) for your findings.""",
    llm=problem_llm,
    verbose=True,
    allow_delegation=False
)

# STAGE 2: Problem Logging & Categorization
cmdb_correlator = Agent(
    role="CMDB Correlator",
    goal="Map incident patterns to specific Configuration Items (CIs) and recent changes.",
    backstory="""You are an expert in ITIL CMDB structures and dependency mapping. 
    Your job is to take incident clusters and find the common infrastructure 
    components or recent Change Requests (CHGs) that link them together.""",
    llm=problem_llm,
    verbose=True,
    allow_delegation=False
)

# STAGE 3: Investigation & Diagnosis
root_cause_investigator = Agent(
    role="Root Cause Investigator",
    goal="Perform a deep-dive 'Five Whys' analysis to find the underlying technical failure.",
    backstory="""You are a specialist in root cause analysis. You move beyond 
    symptoms (like 'service restarted') to find the actual cause (like 'memory 
    leak' or 'connection pool exhaustion'). You use data from the CMDB and 
    Incident logs to prove your theories.""",
    llm=problem_llm,
    verbose=True,
    allow_delegation=False
)

# STAGE 4: Known Error Documentation
known_error_author = Agent(
    role="Known Error Author",
    goal="Document workarounds and root causes in a formal Known Error Record.",
    backstory="""You bridge the gap between deep technical analysis and the 
    Service Desk. You produce clear, actionable documentation for the KEDB 
    (Known Error Database) so that future incidents can be resolved faster.""",
    llm=problem_llm,
    verbose=True,
    allow_delegation=False
)

# STAGE 5: Resolution via Change
change_proposer = Agent(
    role="Change Proposer",
    goal="Generate formal Requests for Change (RFC) to implement permanent fixes.",
    backstory="""You are responsible for the permanent resolution. You design 
    technical fixes, assess implementation risks, and create rollback plans 
    that will be presented to the Change Advisory Board (CAB).""",
    llm=problem_llm,
    verbose=True,
    allow_delegation=False
)