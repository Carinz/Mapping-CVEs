import argilla as rg

from huggingface_login import HF_TOKEN

# TODO: Remove secrets before submission! Can add credentials to git instead!
HF_TOKEN = ''
# Set credentials
# client = rg.Argilla(
#     api_url="https://dorsimantov-workshop_new.hf.space",
#     api_key=""
# )

rg.init(
  api_url="https://dorsimantov-workshop.hf.space",
  api_key="",
  # extra_headers={"Authorization": f"Bearer {HF_TOKEN}"}
  )

dataset = rg.FeedbackDataset.for_text_classification(
    labels=["sadness", "joy"],
    multi_label=False,
    use_markdown=True,
    guidelines=None,
    metadata_properties=None,
    vectors_settings=None,
)
# Create the dataset to be visualized in the UI (uses default workspace)
dataset.push_to_argilla(name="my-first-dataset", workspace="admin")

records = [
    rg.FeedbackRecord(
        fields={
            "text": "I am so happy today",
        },
    ),
    rg.FeedbackRecord(
        fields={
            "text": "I feel sad today",
        },
    )
]
dataset.add_records(records)

# dataset = rg.FeedbackDataset.from_argilla("my-first-dataset", workspace="admin")
# dataset.push_to_huggingface("my-repo/my-first-dataset")

