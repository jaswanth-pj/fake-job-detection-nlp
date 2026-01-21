import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

<<<<<<< HEAD



=======
>>>>>>> 426a65d7aaba082392e065247c3b105ae26314b6
df = pd.read_csv("./jobcheck/dataset/cleaned_fake_job_postings.csv")
if "fraudulent" not in df.columns:
    raise ValueError("Column 'fraudulent' not found. Ensure your dataset has this column.")
<<<<<<< HEAD






=======
>>>>>>> 426a65d7aaba082392e065247c3b105ae26314b6
plt.figure(figsize=(6,4))
counts = df["fraudulent"].value_counts()
<<<<<<< HEAD

plt.bar(["Real (0)"], counts[0], color="skyblue")
plt.bar(["Fake (1)"], counts[1], color="salmon")  

=======
plt.bar(["Real (0)"], counts[0], color="skyblue")
plt.bar(["Fake (1)"], counts[1], color="salmon")   # Change this color as you like!
>>>>>>> 426a65d7aaba082392e065247c3b105ae26314b6
plt.title("Distribution of Fake vs Real Job Posts")
plt.xlabel("Category")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

text_columns = df.select_dtypes(include=["object"]).columns
df["combined_text"] = df[text_columns].apply(lambda row: " ".join(row.values.astype(str)), axis=1)
df["text_length"] = df["combined_text"].apply(lambda x: len(x.split()))
<<<<<<< HEAD


=======
>>>>>>> 426a65d7aaba082392e065247c3b105ae26314b6
plt.figure(figsize=(6,4))
df[df["fraudulent"] == 0]["text_length"].plot(kind="hist", alpha=0.5, label="Real", bins=50)
df[df["fraudulent"] == 1]["text_length"].plot(kind="hist", alpha=0.5, label="Fake", bins=50)
plt.xlabel("Text Length (number of words)")
plt.ylabel("Frequency")
plt.title("Text Length Comparison: Fake vs Real")
plt.legend()
plt.tight_layout()
plt.show()
<<<<<<< HEAD





vectorizer = TfidfVectorizer(stop_words="english", max_features=50)
X_fake = vectorizer.fit_transform(df[df["fraudulent"] == 1]["combined_text"])


words = vectorizer.get_feature_names_out()
scores = np.array(X_fake.mean(axis=0)).flatten()


top_indices = scores.argsort()[::-1][:20]
top_words = words[top_indices]
top_scores = scores[top_indices]


=======
vectorizer = TfidfVectorizer(stop_words="english", max_features=50)
X_fake = vectorizer.fit_transform(df[df["fraudulent"] == 1]["combined_text"])
words = vectorizer.get_feature_names_out()
scores = np.array(X_fake.mean(axis=0)).flatten()
top_indices = scores.argsort()[::-1][:20]
top_words = words[top_indices]
top_scores = scores[top_indices]
>>>>>>> 426a65d7aaba082392e065247c3b105ae26314b6
plt.figure(figsize=(8,5))
plt.barh(top_words, top_scores)
plt.gca().invert_yaxis()
plt.title("Top Common Words in Fake Job Posts (TF-IDF)")
plt.xlabel("TF-IDF Importance Score")
plt.tight_layout()
plt.show()
