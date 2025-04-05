# -*- coding: utf-8 -*-
"""AA Activity2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/156ehkO-HYRSH-_JdIzMt4hL0FXAY8Vln
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF
from google.colab import files
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Upload files
uploaded = files.upload()

import pandas as pd

# Load datasets
resume_df = pd.read_excel("resume.xlsx")
jobs_df = pd.read_excel("jobs.xlsx")

# Show columns
print("🧾 Resume columns:", resume_df.columns.tolist())
print("🧾 Job columns:", jobs_df.columns.tolist())

# Combine job title + description into a single text column
if "job_title" in jobs_df.columns and "job_description" in jobs_df.columns:
    jobs_df["job_text"] = jobs_df["job_title"].fillna('').astype(str) + " " + jobs_df["job_description"].fillna('').astype(str)
else:
    jobs_df["job_text"] = jobs_df.fillna('').astype(str).agg(' '.join, axis=1)

# 🚫 Remove duplicate rows based on both title and description
jobs_df_unique = jobs_df.drop_duplicates(subset=["job_title", "job_description"], keep='first').reset_index(drop=True)

jobs_df_unique["job_text"] = jobs_df_unique["job_text"].str.lower().str.replace(r'\s+', ' ', regex=True).str.strip()

# Then, build the list for vectorization
job_texts = jobs_df_unique["job_text"].tolist()

# Combine resume text from available columns
if "skills" in resume_df.columns and "experience" in resume_df.columns:
    resume_df["resume_text"] = resume_df["skills"].fillna('').astype(str) + " " + resume_df["experience"].fillna('').astype(str)
else:
    resume_df["resume_text"] = resume_df.fillna('').astype(str).agg(' '.join, axis=1)

#Combine only job title + job description for job matching
if "job_title" in jobs_df.columns and "job_description" in jobs_df.columns:
    jobs_df["job_text"] = jobs_df["job_title"].fillna('').astype(str) + " " + jobs_df["job_description"].fillna('').astype(str)
else:
    jobs_df["job_text"] = jobs_df.fillna('').astype(str).agg(' '.join, axis=1)

# TF-IDF Vectorization on job descriptions
job_texts = jobs_df["job_text"].tolist()
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
job_vectors = vectorizer.fit_transform(job_texts)
print(" Model trained using job descriptions.")

print("Upload your resume (PDF)...")
uploaded_resume = files.upload()
resume_filename = list(uploaded_resume.keys())[0]

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

resume_text = extract_text_from_pdf(resume_filename)

# Vectorize uploaded resume
resume_vector = vectorizer.transform([resume_text])
scores = cosine_similarity(resume_vector, job_vectors).flatten()

# Define rating system
def rate_resume(score):
    if score >= 0.7:
        return "Excellent"
    elif score >= 0.5:
        return "Good"
    elif score >= 0.3:
        return "Average"
    else:
        return "Poor"

# Show Top 3 Unique Job Matches by Job Title
print("\n Top 3 Unique Job Matches")

# Get top scores sorted in descending order
sorted_indices = scores.argsort()[::-1]

# Track seen titles and collect top matches
seen_titles = set()
top_matches = []

for idx in sorted_indices:
    title = jobs_df_unique.iloc[idx]['job_title']
    if title not in seen_titles:
        seen_titles.add(title)
        top_matches.append(idx)
    if len(top_matches) == 3:
        break

# Display results
for i, idx in enumerate(top_matches):
    print(f"\n Match {i+1}: {jobs_df_unique.iloc[idx]['job_title']}")
    print(f"Score: {round(scores[idx], 2)}")
    print(f"Snippet: {jobs_df_unique.iloc[idx]['job_description'][:200]}...")
    print("Rating:", rate_resume(scores[idx]))

top_df = pd.DataFrame({
    "Job Title": [jobs_df_unique.iloc[i]["job_title"] for i in top_matches],
    "Match Score": [scores[i] for i in top_matches]
})
plt.figure(figsize=(5, 2.8))
sns.barplot(data=top_df, x="Match Score", y="Job Title", palette="coolwarm")
plt.title("Top 3 Matches", fontsize=12)
plt.tight_layout(); plt.show()

labels = [rate_resume(scores[i]) for i in top_matches]
counts = pd.Series(labels).value_counts()
counts.plot.pie(autopct='%1.0f%%', colors=sns.color_palette("pastel"), ylabel='', title=" Match Quality")
plt.show()

# Save only top match results (without skill gap or visualization)
with open("resume_match_results.txt", "w") as f:
    for i, idx in enumerate(top_matches):
        f.write(f"Match {i+1}: {jobs_df_unique.iloc[idx]['job_title']}\n")
        f.write(f"Score: {round(scores[idx], 2)}\n")
        f.write(f"Rating: {rate_resume(scores[idx])}\n")
        f.write(f"Snippet: {jobs_df_unique.iloc[idx]['job_description'][:200]}...\n\n")
print("Results saved to 'resume_match_results.txt'")