# Preliminaries

1. Install project requirements listed in `requirements.txt` using pip:

    ```bash
    pip install -r requirements.txt
    ```

2. Set your HuggingFace, OpenAI API, and Weights & Biases keys in the `global_config.yml` file.

# AutoPrompt CVE Prompt Optimization Pipeline

1. Set the estimator model (`gpt` for GPT-4o mini or `local` for microsoft/Phi-3-mini-4k-instruct) and the maximal number of related protocols for each CVE in the initial dataset (1 or 2) in the `global_config.yml` file.
2. To change other AutoPrompt parameters, manually edit **all** config files located in `autoprompt_code/AutoPrompt/config`.
3. Run the pipeline using the following command:

    ```bash
    python autoprompt_code/AutoPrompt/project_optimization_pipeline.py
    ```

# Additional Local Model Tools

In the `local_model` folder, you can find tools used for evaluating calibrated prompts for the local model, as well as tools for synthetic data generation via GPT-4o mini—used in our project to generate hard examples which were scarce in the human-annotated dataset.

- `apply_experiments.py` applies the local model to the complete dataset using each of the prompts provided in the `prompt_experiments` array, along with the corresponding `experiment_names` array. Results are output to the `model_responses` folder as CSV files.

The following tools pertain to the synthetic samples part of the project:

- `create_requests_file_for_synthetic_data.py` creates request JSONL files from the provided prompts and number of samples, which can later be fed to the OpenAI API for generation. Files are output to `requests_jsonl`.

- `create_batch_for_synthetic_data.py` feeds the requests to GPT-4o mini. Results are output to `responses_jsonl` as JSONL files.

- `batch_parser.py` parses the JSONL results and saves them to `responses_csv` as CSV files.

- `test_initial_vs_calibrated_on_synthetic_data.py` feeds the parsed CSVs to the local model and saves the results to `model_responses_synthetic`.

- `metrics_synthetic.py` calculates the accuracies for all response CSVs and prints them to the screen.

# Data Manipulation
In order to get to the point of final 400 samples (metrics/data after manipulation/final_all.csv) from the 624 we got under 'all.csv' we used functions from `data_manipulation.py`, but also added missing descriptions manually, and manually tagging some conflicts.

# GPT Experiments
In the 'metrics' folder there are scripts you need to run one after the other to have GPT responses of all experiments:
- `create_requests_file.py` creates all json files of all the experiments, (to sent do GPT through the API). the files are created in folder 'requests_jsonl'. The data is taken from folder "data after manipulation/final_all.csv".
  
- `create_batch.py` creates batches (GPT runs in the background) to all experiments. need to uncomment the specific experiment type you want to create the batch for, then save the batch_id which is printed.
  
- `check_batch.py` checks the status of the batches according to their ids (the id taken from create_batch step) and outputs all the output_file ids for the next step. (this step completes its run successfully only when all the batches are completed).
  
- `retrieve_batch.py` takes all output_file ids from the previous step and translates the GPT responses to csv tables according to the experiments names. All experiments are saved in folder 'batch_experiments'.

# Metrics
In "metrics" folder there is `metrics.py` script, before running it make sure there are all the experiments in 'batch_experiments' folder (which are GPT responses) and all the experiments in 'local_experiments' which are all the responses of the local model.
This script creates all metrics, per model, per experiment according to sub groups, and also creates mean metrics to each experiment. Make sure the folders exist (inside metrics_results) like in our code before running the script.
