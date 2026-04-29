# FinServe Digital Bank – Production Incident & BIA Simulation

An advanced **Agent-Driven Business Continuity & Incident Response** system built on CrewAI. This project simulates a Tier-1 financial institution's response to critical service disruptions using autonomous agents.

## 🛡️ Production Realism & Stability Features

This version implements several "Production Grade" logic enhancements to satisfy complex BCM requirements:

* **Non-Linear Impact Modeling:** The Business Impact Analyst (BIA) calculates financial degradation using exponential scaling ($Hours^{1.8}$), capturing the realistic spike in costs over 1h, 2h, and 4h intervals.
* **ITIL 4 & ISO 22301 Alignment:** Agents are mapped to specialized professional roles (SecOps, BIA Analyst, Emergency Change Manager) and utilize industry-standard frameworks for triage and recovery.
* **Local LLM Optimization:** Architected for **Llama 3.1: 8B (via Ollama)**. Uses sequential task orchestration and Pydantic-structured data contracts to ensure stability on limited hardware.
* **Cascading Dependency Logic:** Tools simulate real-world service relationships where infrastructure failures (e.g., Database) propagate through the application stack (e.g., Mobile Banking).

---

## 🏗️ System Architecture

The simulation is orchestrated through a specialized 6-agent workflow:

1.  **Incident Classifier:** Performs initial triage and determines NIST severity (P1-P5).
2.  **SecOps Analyst:** Manages containment, MITRE ATT&CK mapping, and forensic preservation.
3.  **BIA Analyst:** Executes quantitative financial modeling and regulatory (GDPR/PCI-DSS) risk assessment.
4.  **Recovery Engineer:** Orchestrates DR failover execution and RTO/RPO validation.
5.  **Change Manager:** Documents Emergency RFCs and ensures rollback readiness.
6.  **Crisis Communicator:** Generates multi-audience messaging for Executives, Customers, and Regulators.

---

## 🚀 Setup & Execution

### 1. Environment Setup
```bash
git clone [your-repo-link]
cd itsm-devops-bcm-crewai-starter
pip install -r requirements.txt

### 2. Local LLM Configuration
This project is optimized for local execution to ensure data privacy and cost-efficiency. Ensure [Ollama](https://ollama.com/) is installed and the model is pulled:

```bash
ollama pull llama3.1:8b

### 3. Data & Environment Configuration
To ensure the simulation has the necessary context to perform BIA and technical analysis, configure the following:

* **Package Discovery:** Ensure the `src/__init__.py` file exists in your source directory.
* **Environment Variables:** Copy `.env.example` to `.env` and configure the local paths for your datasets:
    * `INCIDENT_DATA_PATH`: Path to your incident logs CSV.
    * `CMDB_DATA_PATH`: Path to the FinServe configuration management database.
    * `CHANGE_DATA_PATH`: Path to the historical change records.
* **Data Integrity:** Verify that the `data/` directory contains all referenced CSV files required for tool-based querying.

### 4. Run Simulation
Once the environment is configured and the Ollama service is active, trigger the automated response crew. This will initiate the sequential ITIL/BCM lifecycle analysis:

```bash
python main.py

## 📂 Project Structure

The repository is organized to separate agent logic from technical tools, ensuring a modular and scalable architecture:

* **`main.py`**: The primary entry point. Initializes environment variables and kicks off the problem-management simulation.
* **`src/`**: Core package containing all logic.
    * **`__init__.py`**: Mandatory file to initialize the directory as a Python package for relative imports.
    * **`agents.py`**: Defines agent personas, backstories, and assigns the local Llama 3.1 LLM configuration.
    * **`tasks.py`**: Contains the sequential task definitions and structured Pydantic output models.
    * **`tools.py`**: Python-based engine containing the heavy-lifting logic for financial math, CMDB queries, and system actions.
    * **`problem_crew.py`**: Orchestration file that assembles the agents and tasks into a unified, sequential Crew.
    * **`bia_crew.py`**: Specialized orchestration for targeted Business Impact Analysis testing.
* **`data/`**: Storage for the required simulation datasets (CSV format).
* **`.env`**: Local configuration for sensitive paths and API placeholders.
* **`.gitignore`**: Prevents virtual environments, caches, and local data from being committed to the repository.