import sqlite3
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ----------------------------
# 1. Load flagged posts
# ----------------------------
conn = sqlite3.connect("../backend/users.db")


flagged_df = pd.read_sql_query(
    "SELECT text, result FROM predictions WHERE flagged = 1",
    conn
)

conn.close()

if flagged_df.empty:
    print("❌ No flagged posts found. Retraining skipped.")
    exit()

# Convert labels
flagged_df["label"] = flagged_df["result"].map({
    "Fake Job": 1,
    "Real Job": 0
})

flagged_df = flagged_df[["text", "label"]]

# ----------------------------
# 2. Load original dataset
# ----------------------------
orig_df = pd.read_csv("../dataset/cleaned_fake_job_postings.csv")
orig_df = orig_df[["description", "fraudulent"]]
orig_df.columns = ["text", "label"]

# ----------------------------
# 3. Combine datasets
# ----------------------------
combined_df = pd.concat([orig_df, flagged_df], ignore_index=True)
# ----------------------------
# 3.1 Clean NaN / empty text
# ----------------------------
combined_df["text"] = combined_df["text"].astype(str)
combined_df = combined_df[combined_df["text"].str.strip() != ""]

print(f"Training on {len(combined_df)} samples")

# ----------------------------
# 4. Train model again
# ----------------------------
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X = tfidf.fit_transform(combined_df["text"])
y = combined_df["label"]

model = LogisticRegression(
    max_iter=500,
    class_weight="balanced"
)

model.fit(X, y)

# ----------------------------
# 5. Save updated model
# ----------------------------
pickle.dump(model, open("../backend/model/logistic_model.pkl", "wb"))
pickle.dump(tfidf, open("../backend/model/tfidf_vectorizer.pkl", "wb"))

print("✅ Model retrained successfully using flagged posts")
