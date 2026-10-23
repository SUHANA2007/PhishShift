
import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Load the larger, cleaned SMS dataset
df = pd.read_csv("data/messages_full_clean.csv")

# Keep original, verified dataset labels for this experiment
df = df[df["original_label"].isin(["ham", "spam"])].copy()
df = df.dropna(subset=["body_text", "original_label"])
df = df.drop_duplicates(subset=["body_text"])

X = df["body_text"].astype(str)
y = df["original_label"].astype(str)

print("Dataset loaded:", len(df), "messages")
print("\nOriginal label distribution:")
print(y.value_counts())

# Split data before model fitting
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression": Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("model", LogisticRegression(max_iter=1000))
    ]),
    "Multinomial Naive Bayes": Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("model", MultinomialNB())
    ])
}

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test, predictions, pos_label="spam", zero_division=0
    )
    recall = recall_score(
        y_test, predictions, pos_label="spam", zero_division=0
    )
    f1 = f1_score(
        y_test, predictions, pos_label="spam", zero_division=0
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Spam Precision": precision,
        "Spam Recall": recall,
        "Spam F1": f1
    })

    print(f"\n--- {name} ---")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Confusion matrix (labels: ham, spam):")
    print(confusion_matrix(y_test, predictions, labels=["ham", "spam"]))

# Display and save metrics
results_df = pd.DataFrame(results)
print("\nModel comparison:")
print(results_df.to_string(index=False))

Path("reports").mkdir(exist_ok=True)
results_df.to_csv("reports/sms_model_comparison.csv", index=False)
# Save the best model for later use
import joblib

best_model = models["Logistic Regression"]
joblib.dump(best_model, "phishshift_model.pkl")

print("Best model saved successfully!")

print("\nResults saved to reports/sms_model_comparison.csv")
print("Note: These results evaluate SMS spam detection, not phishing detection.")
print("A random split does not test generalization to unseen campaigns.")
