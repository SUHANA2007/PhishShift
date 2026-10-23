
import pandas as pd
from pathlib import Path

input_file = Path("data/messages_full.csv")
output_file = Path("data/messages_full_clean.csv")
log_file = Path("data/full_cleaning_log.txt")

# Load the imported dataset
df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Remove rows with missing message text or labels
df = df.dropna(subset=["body_text", "original_label"])

# Clean message text and labels
df["body_text"] = df["body_text"].astype(str).str.strip()
df["original_label"] = (
    df["original_label"].astype(str).str.strip().str.lower()
)

# Remove empty messages
df = df[df["body_text"] != ""]

# Remove duplicate message text
before = len(df)
df = df.drop_duplicates(subset=["body_text"]).copy()
duplicates_removed = before - len(df)

# Preserve the original label; do not equate spam with phishing
df["phishshift_label"] = df["original_label"].map({
    "ham": "legitimate",
    "spam": "needs_review"
})

# Save cleaned dataset
df.to_csv(output_file, index=False)

# Create a cleaning log
log = (
    f"Original rows: {before}\n"
    f"Duplicate messages removed: {duplicates_removed}\n"
    f"Final rows: {len(df)}\n"
    f"Missing values remaining: {df.isnull().sum().sum()}\n"
)

log_file.write_text(log, encoding="utf-8")

print("\nDuplicate messages removed:", duplicates_removed)
print("Cleaned dataset shape:", df.shape)
print("\nOriginal label distribution:")
print(df["original_label"].value_counts())
print("\nSaved:", output_file)
print("Cleaning log saved:", log_file)
print("\nCleaning completed successfully!")
