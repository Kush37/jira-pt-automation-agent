import subprocess

def run_k6(script_path):
    try:
        # k6 run with 1 user (VU) and 1 iteration
        cmd = ["k6", "run", "--vus", "1", "--iterations", "1", script_path]

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        print("\n--- K6 OUTPUT ---")
        print(result.stdout)

        if result.stderr:
            print("\n--- K6 ERRORS ---")
            print(result.stderr)

    except FileNotFoundError:
        print("Error: k6 not found. Install k6 from https://k6.io/docs/get-started/installation/")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Replace with your k6 script path
    run_k6("script.js")
