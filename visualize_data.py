
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load cleaned dataset
df = pd.read_csv("data/messages_clean.csv")

# Create folder for charts
output_dir = Path("visualizations")
output_dir.mkdir(exist_ok=True)

# Chart 1: Message label distribution
label_counts = df["label"].value_counts()

plt.figure(figsize=(7, 5))
label_counts.plot(kind="bar")
plt.title("PhishShift - Message Label Distribution")
plt.xlabel("Message Label")
plt.ylabel("Number of Messages")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / "label_distribution.png")
plt.show()

# Chart 2: Message length distribution
df["message_length"] = df["body_text"].astype(str).str.len()

plt.figure(figsize=(7, 5))
for label in df["label"].unique():
    df.loc[df["label"] == label, "message_length"].plot(
        kind="hist",
        bins=5,
        alpha=0.6,
        label=label
    )

plt.title("PhishShift - Message Length Distribution")
plt.xlabel("Message Length (characters)")
plt.ylabel("Number of Messages")
plt.legend()
plt.tight_layout()
plt.savefig(output_dir / "message_length_distribution.png")
plt.show()

print("Visualization completed successfully!")
print("Charts saved inside the visualizations folder.")
