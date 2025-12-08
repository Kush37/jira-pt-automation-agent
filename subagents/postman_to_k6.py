import subprocess
from pathlib import Path


def convert_postman_to_k6(postman_collection_path: str, k6_output_path: str) -> None:
    """
    Convert a Postman collection JSON file to a k6 script using the
    `postman-to-k6` Node package.

    :param postman_collection_path: Path to the Postman collection JSON file.
    :param k6_output_path: Path where the k6 script should be written.
    """
    postman_collection = Path(postman_collection_path)
    k6_output = Path(k6_output_path)

    if not postman_collection.is_file():
        raise FileNotFoundError(f"Postman collection not found: {postman_collection}")

    # Build the command for postman-to-k6
    cmd = [
        "postman-to-k6",
        str(postman_collection),
        "-o",
        str(k6_output)
    ]

    try:
        # Run the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=True,
        )
        print("Conversion completed successfully.")
        if result.stdout:
            print("stdout:", result.stdout)
        if result.stderr:
            print("stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error while converting Postman collection to k6 script.")
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        raise


if __name__ == "__main__":
    # Example usage:
    # Converts `collection.json` to `script.js`
    convert_postman_to_k6("collection.json", "k6_script.js")