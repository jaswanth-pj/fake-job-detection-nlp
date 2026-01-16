import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ----------------------------------
# 1. Load cleaned dataset
# ----------------------------------
df = pd.read_csv("../dataset/cleaned_fake_job_postings.csv")

# ----------------------------------
# 2. Select features and target
# ----------------------------------
X = df["description"].astype(str)
y = df["fraudulent"]

# ----------------------------------
# 3. TF-IDF Vectorization
# ----------------------------------
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_tfidf = tfidf.fit_transform(X)

# ----------------------------------
# 4. Train-Test Split (80% / 20%)
# ----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ----------------------------------
# 5. Train Logistic Regression Model
# ----------------------------------
model = LogisticRegression(
    max_iter=500,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ----------------------------------
# 6. Model Evaluation
# ----------------------------------
y_pred = model.predict(X_test)

print("\nLogistic Regression Performance:\n")
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# ----------------------------------
# 7. Save Model and Vectorizer
# ----------------------------------
pickle.dump(model, open("../backend/model/logistic_model.pkl", "wb"))
pickle.dump(tfidf, open("../backend/model/tfidf_vectorizer.pkl", "wb"))

print("\nModel and TF-IDF vectorizer saved successfully!")
