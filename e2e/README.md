#  LLM-Planner on alfred dataset

An end-to-end agent that uses a LLM-Planner.

## Running custom models

Use the `engine` key in the [config](./config/config_alfred.yaml) to change the llm model used. The full config is as follows.
You can provide a custom model path via `model_path`


```yaml
name: alfred
out_dir: "./"
debug: False # Used to debug a single task. Modify the line mentioned by NOTE in src/run_eval.py
save_results: True  # Enable saving results for debugging

llm_planner:
  engine: "gpt-4o-mini"
  vision: False
  dynamic: False
  max_retries: 1  # Maximum number of retries per action
  max_replanning: 5  # Maximum number of dynamic replanning attempts per task
  knn_dataset_path: "src/knn_set.pkl"
  emb_model_name: "paraphrase-MiniLM-L6-v2"
  num_in_context_examples: 9
  use_step_instructions: False # True # False  # Set to False to disable step instructions
  obj_sim_threshold: 0.8  # Threshold for fuzzy object matching (0.0 to 1.0)
  debug: True
  model_path: ""  # for custom models


alfred:
  env_args:
    data: alfred/data/json_2.1.0
    pframe: 300
    fast_epoch: false
    reward_config: alfred/models/config/rewards.json
    max_steps: 1000
    pp_folder: pp
  x_display: '0'
  eval_set: 'valid_unseen'  # valid_seen, valid_unseen
  splits: alfred/data/splits/oct21.json
```


## Running evaluation 

Use the [run_eval](./src/run_eval.py) script 

```sh
python run_eval --help
    --config CONFIG
    --dry_run DRY_RUN # for debugging
```

You can view aggregated stats with the [print_resulst](print_results.py) script

```sh
python print_results --help
    --path PATH # result directory
```



## What's Here

- Fully end-to-end agent that uses a LLM-Planner.
- Supports dynamic re-planning, image input, and more.

## Usage

### Setup   

Please be in the `e2e/` directory to run the following commands.

```
conda create -n llm-planner python=3.8 -y
conda activate llm-planner
pip install -r requirements.txt
```

### Download ALFRED Dataset

```
cd alfred/data
bash download_data.sh json
```

### Setup OpenAI Key
```
export OPENAI_API_KEY=<your-openai-api-key>
```
If you want to use a different LLM, modify the `llm()` function in `run_eval.py`.

Note that the prompt will likely need further optimization if you plan to use other LLMs.

### Sanity Checks
#### Simulator Check

```
python check_thor.py
```
This will check if your THOR environment is setup correctly.

#### Agent Check

```
python src/run_eval.py --config config/config_alfred.yaml --dry_run
```
This will run the agent on 3 tasks and save the results to `results/`.

**NOTE**: It is recommended to dry run the agent first since it will preprocess the dataset.

### Full Evaluation

```
python src/run_eval.py --config config/config_alfred.yaml
```
This will run the agent on all tasks and save the results to `results/`.

Check out the `config/config_alfred.yaml` for more options.

## FAQs

**Q1:** AssertionError: Invalid DISPLAY 0 - cannot find X server with xdpyinfo

**A1:** Check your display number with `xdpyinfo` and set it by running `export DISPLAY=:<your-display-number>` before executing the script.

**Q2:** How does the LLM generated plans get grounded?

**A2:** The function `llm_skill_interact` in `src/alfred/thor_connector.py` is the function that grounds the LLM generated plans.

**Q3:** What system was this tested on?

**A3:** This was tested on a MacBook Pro with an M1 Pro chip and on Ubuntu 22.04.

**Q4:** How does the choice of LLM affect performance?

**A4:** Our prompt was optimized for `text-davinci-003`, and we found that the GPT-4 family performs slightly worse in planning tasks. We recommend using `gpt-3.5-turbo` if possible, or adapting the prompt based on newer methods cited in our README.


