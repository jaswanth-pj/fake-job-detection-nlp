import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("./jobcheck/dataset/fake_job_postings.csv")
print("Shape before cleaning:", df.shape)

# ------------------------- #
# 1. Remove duplicate rows
# ------------------------- #
df.drop_duplicates(inplace=True)

# ------------------------- #
# 2. Remove columns with too many missing values (optional)
# ------------------------- #
missing_percent = df.isnull().mean() * 100
cols_to_drop = missing_percent[missing_percent > 60].index
df.drop(columns=cols_to_drop, inplace=True)

# ------------------------- #
# 3. Fill missing values
# ------------------------- #

# Fill text columns with "Unknown"
text_cols = df.select_dtypes(include=['object']).columns
df[text_cols] = df[text_cols].fillna("Unknown")

# Fill numeric columns with median
num_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# ------------------------- #
# 4. Clean text (basic cleaning)
# ------------------------- #

import re

def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)   # remove special chars
    text = re.sub(r'\s+', ' ', text).strip()      # remove extra spaces
    return text

for col in text_cols:
    df[col] = df[col].apply(clean_text)

# ------------------------- #
# 5. Save the cleaned dataset
# ------------------------- #

df.to_csv("./jobcheck/dataset/cleaned_fake_job_postings.csv", index=False)

print("Shape after cleaning:", df.shape)
print("Cleaned dataset saved successfully!")


