
import pandas as pd
from pathlib import Path

# Input and output files
input_file = Path("data/messages_sample.csv")
output_file = Path("data/messages_clean.csv")
log_file = Path("data/cleaning_log.txt")

# Check whether the dataset exists
if not input_file.exists():
    raise FileNotFoundError(
        "Dataset not found. Run prepare_data.py first."
    )

# Load the dataset
df = pd.read_csv(input_file)

print("1. Original dataset shape:", df.shape)

# Check required columns
required_columns = [
    "message_id",
    "campaign_group",
    "channel",
    "body_text",
    "label"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# Count missing values before cleaning
missing_before = int(df[required_columns].isna().sum().sum())

# Remove rows missing essential information
df = df.dropna(
    subset=["message_id", "campaign_group", "channel", "body_text", "label"]
).copy()

# Normalize text and labels
df["body_text"] = df["body_text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip().str.lower()
df["channel"] = df["channel"].astype(str).str.strip().str.lower()

# Remove empty messages
df = df[df["body_text"] != ""]

# Keep only valid labels
valid_labels = ["phishing", "legitimate"]
df = df[df["label"].isin(valid_labels)]

# Count exact duplicate messages before removing them
duplicate_count = int(
    df.duplicated(subset=["body_text"], keep="first").sum()
)

# Remove exact duplicate message text
df = df.drop_duplicates(
    subset=["body_text"], keep="first"
).copy()

# Save cleaned data
df.to_csv(output_file, index=False)

# Save a simple cleaning log
with open(log_file, "w", encoding="utf-8") as log:
    log.write("PhishShift Cleaning Log\n")
    log.write(f"Original rows: {len(pd.read_csv(input_file))}\n")
    log.write(f"Missing required values: {missing_before}\n")
    log.write(f"Exact duplicate messages removed: {duplicate_count}\n")
    log.write(f"Final rows: {len(df)}\n")

# Display results
print("2. Missing values found:", missing_before)
print("3. Duplicate messages removed:", duplicate_count)
print("4. Cleaned dataset shape:", df.shape)
print("\n5. Label distribution:")
print(df["label"].value_counts())
print("\n6. Cleaned data saved to:", output_file)
print("7. Cleaning log saved to:", log_file)
print("\nCleaning completed successfully!")
