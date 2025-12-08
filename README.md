# JIRA Performance Testing Automation Agent

This utility is an AI-driven agent designed to automate the process of performance testing. It takes a JIRA story as input, validates attached Postman collections, converts them to k6 scripts, executes the tests, and analyzes the results against defined SLAs.

## Prerequisites

Before running this agent, ensure you have the following installed on your system:

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2.  **Node.js & npm** (Required for `postman-to-k6`): [Download Node.js](https://nodejs.org/)
3.  **k6** (Load testing tool): [Download k6](https://k6.io/docs/get-started/installation/)
4.  **OpenAI API Key**: You will need a valid API key from OpenAI.

## Installation

Follow these detailed steps to set up the environment and dependencies.

### 1. Clone or Download the Repository
Navigate to the project directory:
```bash
cd jira-pt-automation-agent
```

### 2. Set up a Python Virtual Environment
It is recommended to use a virtual environment to manage Python dependencies.

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
Install the required Python packages using `pip`:
```bash
pip install -r Requirements.txt
```

### 4. Install `postman-to-k6`
This tool is required to convert Postman collections into k6 scripts. Install it globally using npm:

```bash
npm install -g postman-to-k6
```

> **Note:** On some systems, you might need to use `sudo` (Linux/macOS) or run PowerShell as Administrator (Windows) for global installation.

### 5. Verify Installations
Ensure that both `k6` and `postman-to-k6` are correctly installed and accessible in your PATH.

```bash
k6 version
postman-to-k6 --version
```

### 6. Configure Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

To run the agent, execute the `main.py` script:

```bash
python main.py
```

The agent will:
1.  Read the JIRA story context (currently mocked in `main.py`).
2.  Validate the Postman collection.
3.  Convert the collection to a k6 script.
4.  (Future) Execute the test and analyze results.
