from subagents.k6_smoke_runner import run_k6

if __name__ == "__main__":
    # Placeholder JIRA Story dict (real system would pass a richer object/context)
    print("Run the k6 test")
    run_k6("k6_script.js")
