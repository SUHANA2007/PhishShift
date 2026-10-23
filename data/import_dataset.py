
import pandas as pd
from pathlib import Path

# Input and output paths
input_file = Path("data/raw/SMSSpamCollection")
output_file = Path("data/messages_full.csv")

# Read the original SMS dataset
df = pd.read_csv(
    input_file,
    sep="\t",
    header=None,
    names=["original_label", "body_text"],
    encoding="utf-8"
)

# Add unique message IDs
df.insert(0, "message_id", [f"SMS{i:05d}" for i in range(1, len(df) + 1)])

# Preserve the original labels
df["original_label"] = df["original_label"].str.lower().str.strip()

# Create a separate label for future review.
# Do NOT automatically call every spam message phishing.
df["phishshift_label"] = df["original_label"].map({
    "ham": "legitimate",
    "spam": "needs_review"
})

# Add campaign placeholders; these are not verified campaign IDs.
df["campaign_group"] = "unknown"
df["channel"] = "SMS"

# Save the imported dataset
output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)

print("Dataset imported successfully!")
print("Total messages:", len(df))
print("\nOriginal label counts:")
print(df["original_label"].value_counts())
print("\nSaved to:", output_file)
print("\nPreview:")
print(df.head())
