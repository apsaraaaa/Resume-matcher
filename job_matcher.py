import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF for PDF reading
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# === Load Resume and Job Data ===
resume_df = pd.read_excel("resume.xlsx")
jobs_df = pd.read_excel("jobs.xlsx")

print("🧾 Resume columns:", resume_df.columns.tolist())
print("🧾 Job columns:", jobs_df.columns.tolist())

# === Prepare Job Text Column ===
if "job_title" in jobs_df.columns and "job_description" in jobs_df.columns:
    jobs_df["job_text"] = jobs_df["job_title"].fillna('') + " " + jobs_df["job_description"].fillna('')
else:
    jobs_df["job_text"] = jobs_df.fillna('').astype(str).agg(' '.join, axis=1)

jobs_df_unique = jobs_df.drop_duplicates(subset=["job_title", "job_description"], keep='first').reset_index(drop=True)
jobs_df_unique["job_text"] = jobs_df_unique["job_text"].str.lower().str.replace(r'\s+', ' ', regex=True).str.strip()

# === Combine Resume Text Columns ===
if "skills" in resume_df.columns and "experience" in resume_df.columns:
    resume_df["resume_text"] = resume_df["skills"].fillna('') + " " + resume_df["experience"].fillna('')
else:
    resume_df["resume_text"] = resume_df.fillna('').astype(str).agg(' '.join, axis=1)

# === TF-IDF Vectorization ===
job_texts = jobs_df_unique["job_text"].tolist()
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
job_vectors = vectorizer.fit_transform(job_texts)
print(" Model trained using job descriptions.")

# === Load Resume PDF Locally ===
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

resume_filename = resume_filename = r"C:\Users\lenovo\Downloads\Sujanya.S resume.pdf"
resume_text = extract_text_from_pdf(resume_filename)

# === Vectorize Resume ===
resume_vector = vectorizer.transform([resume_text])
scores = cosine_similarity(resume_vector, job_vectors).flatten()

# === Rating Logic ===
def rate_resume(score):
    if score >= 0.7:
        return "Excellent"
    elif score >= 0.5:
        return "Good"
    elif score >= 0.3:
        return "Average"
    else:
        return "Poor"

# === Get Top 3 Unique Job Matches ===
sorted_indices = scores.argsort()[::-1]
seen_titles = set()
top_matches = []

for idx in sorted_indices:
    title = jobs_df_unique.iloc[idx]['job_title']
    if title not in seen_titles:
        seen_titles.add(title)
        top_matches.append(idx)
    if len(top_matches) == 3:
        break

# === Display Results ===
for i, idx in enumerate(top_matches):
    print(f"\n🔹 Match {i+1}: {jobs_df_unique.iloc[idx]['job_title']}")
    print(f"Score: {round(scores[idx], 2)}")
    print(f"Snippet: {jobs_df_unique.iloc[idx]['job_description'][:200]}...")
    print("Rating:", rate_resume(scores[idx]))

# === Barplot for Top 3 ===
top_df = pd.DataFrame({
    "Job Title": [jobs_df_unique.iloc[i]["job_title"] for i in top_matches],
    "Match Score": [scores[i] for i in top_matches]
})
plt.figure(figsize=(6, 3))
sns.barplot(data=top_df, x="Match Score", y="Job Title", palette="coolwarm")
plt.title("Top 3 Job Matches")
plt.tight_layout()
plt.show()

# === Save Results to Text File ===
with open("resume_match_results.txt", "w") as f:
    for i, idx in enumerate(top_matches):
        f.write(f"Match {i+1}: {jobs_df_unique.iloc[idx]['job_title']}\n")
        f.write(f"Score: {round(scores[idx], 2)}\n")
        f.write(f"Rating: {rate_resume(scores[idx])}\n")
        f.write(f"Snippet: {jobs_df_unique.iloc[idx]['job_description'][:200]}...\n\n")
print(" Results saved to 'resume_match_results.txt'")






