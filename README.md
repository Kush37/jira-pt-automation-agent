# JIRA Performance Testing Automation Agent

This utility is an AI-driven agent designed to automate the process of performance testing. It takes a JIRA story as input, validates attached Postman collections, converts them to k6 scripts, executes the tests, and analyzes the results against defined SLAs.


## Prerequisites

Before running this agent, ensure you have the following installed on your system:

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2.  **Node.js & npm** (Required for `postman-to-k6`): [Download Node.js](https://nodejs.org/)
3.  **k6** (Load testing tool):
    -   **Windows**:
        -   Using Winget: `winget install k6 --source winget`
        -   Using Chocolatey: `choco install k6`
        -   Or download the MSI installer from [k6.io](https://k6.io/docs/get-started/installation/)
    -   **macOS**: `brew install k6`
    -   **Linux**:
        ```bash
        sudo gpg -k
        sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
        ```
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
You can either use a `.env` file or export the key directly in your shell.

**Option A: Using `.env` file (Recommended)**
Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Option B: Exporting directly in shell**

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your_openai_api_key_here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=your_openai_api_key_here
```

**macOS/Linux:**
```bash
export OPENAI_API_KEY=your_openai_api_key_here
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
