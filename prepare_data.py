
import pandas as pd
from pathlib import Path

# Create the data folder if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Small sample dataset for testing the project setup
messages = [
    {
        "message_id": "M001",
        "campaign_group": "sample_a",
        "channel": "SMS",
        "body_text": "Your account will be blocked. Verify your password now.",
        "label": "phishing",
    },
    {
        "message_id": "M002",
        "campaign_group": "sample_b",
        "channel": "Email",
        "body_text": "Your meeting is scheduled for tomorrow at 10 AM.",
        "label": "legitimate",
    },
    {
        "message_id": "M003",
        "campaign_group": "sample_c",
        "channel": "SMS",
        "body_text": "You have won a prize. Pay a fee to claim it.",
        "label": "phishing",
    },
    {
        "message_id": "M004",
        "campaign_group": "sample_d",
        "channel": "Email",
        "body_text": "Please find the class timetable attached.",
        "label": "legitimate",
    },
    {
        "message_id": "M005",
        "campaign_group": "sample_e",
        "channel": "SMS",
        "body_text": "Urgent: confirm your login details immediately.",
        "label": "phishing",
    },
    {
        "message_id": "M006",
        "campaign_group": "sample_f",
        "channel": "Email",
        "body_text": "Thank you for attending today's workshop.",
        "label": "legitimate",
    },
]

df = pd.DataFrame(messages)
output_path = DATA_DIR / "messages_sample.csv"
df.to_csv(output_path, index=False)

print("Sample dataset created successfully!")
print(f"Saved to: {output_path}")
print(f"Total messages: {len(df)}")
print("\nLabel distribution:")
print(df["label"].value_counts())
print("\nDataset preview:")
print(df.head())
