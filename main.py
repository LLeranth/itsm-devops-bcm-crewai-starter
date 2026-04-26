import os
from dotenv import load_dotenv
from src.problem_crew import create_problem_crew

# Load environment variables
load_dotenv()

def run():
    print("--- Starting FinServe Problem Management Analysis ---")
    
    # Define inputs for the agents
    inputs = {
        'incident_report_path': os.getenv('INCIDENT_DATA_PATH'),
        'cmdb_path': os.getenv('CMDB_DATA_PATH'),
        'change_log_path': os.getenv('CHANGE_DATA_PATH')
    }

    # Initialize the crew
    problem_management_crew = create_problem_crew()
    
    # Run the crew
    result = problem_management_crew.kickoff(inputs=inputs)
    
    print("\n--- FINAL PROBLEM MANAGEMENT REPORT ---")
    print(result)

if __name__ == "__main__":
    run()