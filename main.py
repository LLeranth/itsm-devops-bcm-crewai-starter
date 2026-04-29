import os
from dotenv import load_dotenv
from crewai import LLM  # <--- Add this import
from src.problem_crew import create_problem_crew

def run():
    load_dotenv()

    # 1. Manually define the local LLM connection
    # This forces CrewAI to use Ollama's local endpoint
    ollama_llm = LLM(
        model=os.getenv('OPENAI_MODEL_NAME', 'ollama/llama3.1'),
        base_url=os.getenv('OPENAI_API_BASE', 'http://localhost:11434/v1'),
        api_key=os.getenv('OPENAI_API_KEY', 'ollama'),
        timeout=300
    )

    inputs = {
        'incident_description': (
            "Multiple Tier-1 services (Core Banking API ID: 'API-101', Mobile Banking ID: 'MOB-202') "
            "are reporting ERR-403-CRYPT errors. Encrypted file extensions (.finserve_locked) detected "
            "on Transaction Database (ID: 'DB-PAY-99'). This appears to be a ransomware attack."
        ),
        'incident_report_path': os.getenv('INCIDENT_DATA_PATH', 'data/finserve_incidents_q1_2026.csv'),
        'cmdb_path': os.getenv('CMDB_DATA_PATH', 'data/finserve_cmdb.csv'),
        'change_log_path': os.getenv('CHANGE_DATA_PATH', 'data/finserve_changes.csv'),
        'current_date': '2026-04-29' 
    }

    print("\n" + "="*50)
    print("🚀 FINSERVE PRODUCTION INCIDENT RESPONSE CREW ACTIVATED")
    print("="*50 + "\n")

    # 2. Pass the llm object into your crew creator
    # Note: You may need to update src/problem_crew.py to accept this argument!
    problem_crew = create_problem_crew(llm=ollama_llm)

    try:
        # 3. Kick off the sequential process
        result = problem_crew.kickoff(inputs=inputs)

        # 4. Display the final synthesized report
        print("\n" + "#"*50)
        print("## FINAL INCIDENT RESPONSE & BIA REPORT")
        print("#"*50 + "\n")
        print(result)
        
        print("\n✅ Process Complete. Check the /output folder for RFCs and Known Error records.")

    except Exception as e:
        # Catching the ReadTimeout specifically for your machine
        if "ReadTimeout" in str(e):
            print("❌ Timeout Error: The local LLM took too long to respond.")
            print("Check that Ollama is running and consider reducing the number of tasks.")
        else:
            print(f"❌ An error occurred during the crew execution: {e}")

if __name__ == "__main__":
    run()