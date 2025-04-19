from pathlib import Path
import json
import numpy as np
import argparse

RESULT_PATH = (
    "/home/zacravi/projects/llm-planning-baselines/LLM-Planner/e2e/valid_unseen/results"
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="")

    args = parser.parse_args()

    if args.path == "":
        result_path = RESULT_PATH
    else:
        result_path = args.path

    result_files = sorted(Path(result_path).rglob("*json"))

    success = []

    for file_path in result_files:
        with open(file_path) as f:
            try:
                data = json.load(f)

                success.append(data["success"])

                debug = 0
            except Exception as ex:
                debug = 0

    success = np.array(success)

    print(f"===")
    print(f"Num. trials: {len(success)}")
    print(f"avg. success: {success.mean():0.2f}")
    print(f"Num. successful trials: {success.mean() * len(success)}")
