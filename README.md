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
