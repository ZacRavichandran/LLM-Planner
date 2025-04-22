#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define base paths - adjust if your script is not run from the workspace root
WORKSPACE_ROOT="/home/chiche/LLM-Planner"
BASE_DIR="$WORKSPACE_ROOT/alfred-episodic-random/alfred_iterative_training"
BASE_CONFIG="$WORKSPACE_ROOT/e2e/config/config_alfred_static.yaml"
EVAL_SCRIPT="$WORKSPACE_ROOT/e2e/xvfb-run-safe python $WORKSPACE_ROOT/e2e/src/run_eval.py"
TEMP_CONFIG_DIR="/tmp/alfred_eval_configs"
OUTPUT_BASE_DIR="$BASE_DIR/output"

# Clean up previous temp configs if they exist and create the directory
rm -rf "$TEMP_CONFIG_DIR"
mkdir -p "$TEMP_CONFIG_DIR"

echo "Launching evaluations in parallel..."

# Find all episode directories
find "$BASE_DIR" -maxdepth 1 -type d -name 'episode_*' | while read -r episode_dir; do
    if [ -d "$episode_dir" ]; then
        episode_name=$(basename "$episode_dir") # e.g., episode_1
        model_path="$episode_dir" # Assuming the directory itself is the model path
        output_dir="$OUTPUT_BASE_DIR/$episode_name"
        temp_config_file="$TEMP_CONFIG_DIR/config_${episode_name}.yaml"

        echo "Preparing evaluation for $episode_name..."
        echo "  Model Path: $model_path"
        echo "  Output Dir: $output_dir"
        echo "  Temp Config: $temp_config_file"

        # Create output directory
        mkdir -p "$output_dir"

        # Copy base config to temporary location
        cp "$BASE_CONFIG" "$temp_config_file"

        # Modify model_path and out_dir using sed with # as delimiter for paths
        # Use absolute paths
        sed -i "s#model_path:.*#model_path: "$model_path"#" "$temp_config_file"
        sed -i "s#out_dir:.*#out_dir: "$output_dir"#" "$temp_config_file"

        # Launch the evaluation in the background
        echo "Starting evaluation for $episode_name..."
        ( # Run in a subshell to isolate environment
          cd "$WORKSPACE_ROOT/e2e" || exit 1 # Change directory to e2e
          export PYTHONPATH="$WORKSPACE_ROOT/e2e/src:$PYTHONPATH" # Add e2e/src to PYTHONPATH
          # Use absolute paths for script and config to ensure they are found after cd
          "$WORKSPACE_ROOT/e2e/xvfb-run-safe" python "$WORKSPACE_ROOT/e2e/src/run_eval.py" --config "$temp_config_file"
          echo "Evaluation finished for $episode_name (PWD: $(pwd))."
          # Clean up the specific temp file for this job
          echo "Cleaning up $temp_config_file"
          rm "$temp_config_file"
        ) &
    fi
done

# Wait for all background jobs to complete
echo "Waiting for all evaluations to finish..."
wait

# Clean up temporary config files - REMOVED central cleanup
# echo "Cleaning up temporary configuration files..."
# rm -rf "$TEMP_CONFIG_DIR"

echo "All evaluations completed." 