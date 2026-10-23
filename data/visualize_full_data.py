
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/messages_full_clean.csv")

output_dir = Path("visualizations")
output_dir.mkdir(exist_ok=True)

# Chart 1: Original label distribution
df["original_label"].value_counts().plot(
    kind="bar",
    title="SMS Dataset: Original Label Distribution"
)
plt.xlabel("Original label")
plt.ylabel("Number of messages")
plt.tight_layout()
plt.savefig(output_dir / "full_label_distribution.png")
plt.close()

# Chart 2: Message length distribution
df["message_length"] = df["body_text"].astype(str).str.len()

df["message_length"].plot(
    kind="hist",
    bins=30,
    title="SMS Message Length Distribution"
)
plt.xlabel("Characters per message")
plt.ylabel("Number of messages")
plt.tight_layout()
plt.savefig(output_dir / "full_message_length.png")
plt.close()

print("Visualizations created successfully!")
print("Saved in:", output_dir.resolve())
print("Messages:", len(df))
print("\nOriginal labels:")
print(df["original_label"].value_counts())
