
# Performance Testing AI Agent (DeepAgents + k6) — Skeleton / Placeholders Only

import os
import json
from typing import Dict, Any

from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate

from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent


from dotenv import load_dotenv
from subagents.postman_to_k6 import convert_postman_to_k6



load_dotenv()


# -----------------------------------------------------------------------------
# 0) Orchestrator instructions
# -----------------------------------------------------------------------------
ORCHESTRATOR_PROMPT = """
You are the Performance Testing Orchestrator for k6-based tests.

Input context: A JIRA story with fields:
- Story Number
- Story Title
- Story Description
- Comments
- Attachment(s) (e.g., Postman Collection)

Goals:
1) Determine whether the story contains sufficient information to run performance testing.
2) If sufficient, plan next steps with TODOs and delegate to sub-agents via `task()`.
3) If insufficient, clearly call out missing items and request human intervention.

Validation checklist:
- Postman Collection present in attachments (for API tests)? If missing, request upload/confirmation.
- Load profile details present or derivable (e.g., VUs, duration, ramping profile)? If missing, ask for human input.
- SLA present in Description or Comments? If missing, ask for SLA or provide default policy and request approval.
- Environment/endpoint URLs and authentication details available?
- Any test data prerequisites described?

Execution outline:
- Check the JIRA Story details to understand the requirement and plan next steps.
- Validate Postman collection if present.
- Develop k6 script from Postman collection (API flows) if Postman collection is present.
- Capture/derive load details from Description/Comments using LLM.
- Capture SLA from Description/Comments if present.
- Execute k6 script (when safe; may require HITL approval).
- Analyze k6 results.
- Validate results against SLA; if failing, propose remediation steps or re-run recommendation.

Use built-in DeepAgents capabilities:
- Plan steps using `write_todos`.
- Use `task()` to delegate to sub-agents.
- Offload large artifacts to files (e.g., generated scripts, result JSON) via filesystem tools.

Be explicit:
- If information is missing, stop and ask for the exact missing item(s), e.g., "Please upload the Postman collection JSON".
"""

# -----------------------------------------------------------------------------
# 1) Placeholder tools for each sub-agent (PRINT ONLY; return stub)
# -----------------------------------------------------------------------------

def validate_postman_collection(postman_path: str) -> Dict[str, Any]:
    """
    Validates a Postman collection file.
    """
    print(f"[Validate Postman Collection] Checking: {postman_path}")
    
    if not os.path.exists(postman_path):
        return {"status": "error", "message": f"File not found: {postman_path}"}
        
    try:
        with open(postman_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Basic schema check for v2.0/v2.1 collections
        if "info" not in data or "item" not in data:
             return {"status": "error", "message": "Invalid Postman collection format: missing 'info' or 'item' fields."}
             
        name = data.get("info", {}).get("name", "Unknown")
        col = {
            "status": "valid", 
            "message": f"Successfully validated collection: {name}",
            "collection_name": name,
            "item_count": len(data.get("item", []))
        }
        print(col)
        return col
        
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON format."}
    except Exception as e:
        return {"status": "error", "message": f"Validation failed: {str(e)}"}

def develop_k6_script_from_postman(postman_path: str, output_k6_path: str) -> Dict[str, Any]:
    """
    Converts a Postman collection to a k6 script.
    """
    print(f"[Develop k6 Script] From: {postman_path} -> To: {output_k6_path}")
    convert_postman_to_k6(postman_path, "k6_script.js")
    res = {"status": "success", "message": "k6 script generated from Postman collection (placeholder)."}
    print(res)
    return res
    
def capture_load_details_from_story(story: Dict[str, Any]) -> Dict[str, Any]:
    """
    Captures load testing details from a JIRA story.
    """
    print(f"[Capture Load Details] Story fields: {list(story.keys())}")
    res = {
        "status": "success",
        "message": "Load details captured from story (placeholder).",
        "load_profile": {"vus": 50, "duration": "1m"}  # placeholder only
    }
    print(res)
    return res

def execute_k6_script(k6_script_path: str, env: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes a k6 script with the given environment variables.
    """
    print(f"[Execute k6] Script: {k6_script_path} with env: {env}")
    res = {"status": "success", "message": "k6 executed successfully.", "results_path": "/tmp/k6-results.json"}
    print(res)
    return res

def analyze_k6_results(results_path: str) -> Dict[str, Any]:
    """
    Analyzes k6 test results.
    """
    print(f"[Analyze k6 Results] Results file: {results_path}")
    res = {
        "status": "succesful",
        "message": "k6 results analyzed succesfully.",
        "summary": {"http_req_duration_p95": 250}  # placeholder metric
    }
    print(res)
    return res

def capture_sla_from_story(story: Dict[str, Any]) -> Dict[str, Any]:
    """
    Captures SLA requirements from a JIRA story.
    """
    print(f"[Capture SLA] Inspecting story description/comments for SLA. Fields: {list(story.keys())}")
    res = {
        "status": "placeholder",
        "message": "SLA captured from story (placeholder).",
        "sla": {"http_req_duration_p95": 300}  # placeholder SLA
    }
    print(res)
    return res

def validate_results_with_sla(results_summary: Dict[str, Any], sla: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates test results against SLA requirements.
    """
    print(f"[Validate Results vs SLA] Results: {results_summary} | SLA: {sla}")
    res = {"status": "success", "message": "Results validated with SLA successfully."}
    print(res)
    return res

# -----------------------------------------------------------------------------
# 2) Configure sub-agents (each with its own tool placeholders)
# -----------------------------------------------------------------------------

SUBAGENTS = [
    {
        "name": "validate-postman",
        "description": "Validates Postman collection from JIRA attachment.",
        "system_prompt": (
            "You validate whether a Postman collection is usable for k6 conversion. "
            "Check structure and required environment variables. Provide clear errors if invalid."
        ),
        "tools": [validate_postman_collection],
    },
    {
        "name": "k6-script-dev",
        "description": "Converts Postman collection into k6 script.",
        "system_prompt": (
            "You transform the Postman collection into a k6 script, preserving auth and request flow. "
            "Place generated script into a file for later execution."
        ),
        "tools": [develop_k6_script_from_postman],
    },
    {
        "name": "load-profiler",
        "description": "Captures load parameters (VUs, duration, executors) from story Description and Comments.",
        "system_prompt": (
            "You extract or infer load details (e.g., VUs, duration, ramp profiles) from the story. "
            "If missing, explicitly ask for human input."
        ),
        "tools": [capture_load_details_from_story],
    },
    {
        "name": "k6-executor",
        "description": "Executes k6 script safely.",
        "system_prompt": (
            "You run the k6 script with the declared load profile. "
            "Use safe defaults and log the output path. If environment or endpoints are missing, request human input."
        ),
        "tools": [execute_k6_script],
    },
    {
        "name": "k6-analyzer",
        "description": "Analyzes k6 outputs and produces a structured summary.",
        "system_prompt": (
            "You read the k6 result artifacts and summarize key metrics (latency percentiles, error rates). "
            "Write large outputs to files; return a compact summary."
        ),
        "tools": [analyze_k6_results],
    },
    {
        "name": "sla-extractor",
        "description": "Captures SLA targets from story text, if present.",
        "system_prompt": (
            "You locate SLA in Description/Comments (e.g., p95 latency) and return a structured SLA object. "
            "If absent, request human-defined SLA."
        ),
        "tools": [capture_sla_from_story],
    },
    {
        "name": "results-validator",
        "description": "Validates analyzed results against SLA.",
        "system_prompt": (
            "You compare the k6 summary with the SLA and state PASS/FAIL. "
            "If FAIL, recommend actions (e.g., increase resources, fix bottlenecks) and possible re-run conditions."
        ),
        "tools": [validate_results_with_sla],
    },
]

# -----------------------------------------------------------------------------
# 3) Initialize model and create the Deep Agent
# -----------------------------------------------------------------------------
# DeepAgents lets you use any LangChain chat model (OpenAI/Anthropic/etc.).
# It also provides built-in planning, filesystem tools, and sub-agent delegation via middleware.
# See DeepAgents overview & customization docs.
# (Choose a model string that matches your environment, e.g., "openai:gpt-4o" or "anthropic:claude-3-5-sonnet")
# model = init_chat_model("openai:gpt-4o")
model = ChatOpenAI(model="gpt-5.1", temperature=0)

# chat = init_chat_model(
#     model="gpt-4o-mini",   # Model name (depends on provider)
#     temperature=0.7       # Creativity level
#      # API key for the provider
# )

agent = create_deep_agent(
    model=model,
    system_prompt=ORCHESTRATOR_PROMPT,
    subagents=SUBAGENTS,
)


# -----------------------------------------------------------------------------
# 4) Example invocation (skeleton)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Placeholder JIRA Story dict (real system would pass a richer object/context)
    jira_story = {
        "story_number": "PROJ-1234",
        "title": "Performance test API X with expected peak load",
        "description": "Ensure API X can handle 50 VUs, 1m duration; SLA: p95 < 300ms.",
        "comments": ["Consider auth token rotation", "Postman attached"],
        "attachments": [{"type": "postman_collection", "path": "C:\\Users\\Kushal\\Desktop\\JIRA Automation\\collection.json"}],
    }

    # The DeepAgent will plan and delegate to sub-agents via `task()` based on the prompt.
    result = agent.invoke({"messages": [{"role": "user", "content": f"Run performance testing for:\n{jira_story}"}]})
    print("\n=== Orchestrator Output (placeholder run) ===\n")
    print(result["messages"][-1].content)


