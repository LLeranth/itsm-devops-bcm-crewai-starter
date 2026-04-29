import os
from dotenv import load_dotenv
from src.problem_crew import create_problem_crew

def run():
    """
    Main entry point for the FinServe Problem Management Crew.
    """
    # 1. Load environment variables
    load_dotenv()

    # 2. Prepare the inputs
    # Added 'incident_description' so the Incident Classifier knows what happened
    inputs = {
        'incident_description': (
            "Multiple Tier-1 services (Core Banking API, Mobile Banking) are reporting "
            "ERR-403-CRYPT errors. Encrypted file extensions (.finserve_locked) detected "
            "on Transaction Database volumes. This appears to be a ransomware attack."
        ),
        'incident_report_path': os.getenv('INCIDENT_DATA_PATH', 'data/finserve_incidents_q1_2026.csv'),
        'cmdb_path': os.getenv('CMDB_DATA_PATH', 'data/finserve_cmdb.csv'),
        'change_log_path': os.getenv('CHANGE_DATA_PATH', 'data/finserve_changes.csv'),
        'current_date': '2026-04-29' 
    }

    print("\n" + "="*50)
    print("🚀 FINSERVE PRODUCTION INCIDENT RESPONSE CREW ACTIVATED")
    print("="*50 + "\n")

    # 3. Create the crew using the function from src/problem_crew.py
    # This now initializes your 6 specialized agents and the BCM workflow
    problem_crew = create_problem_crew()

    try:
        # 4. Kick off the sequential process
        result = problem_crew.kickoff(inputs=inputs)

        # 5. Display the final synthesized report
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