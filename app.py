# -*- coding: utf-8 -*-


#from google.colab import drive
#drive.mount('/content/drive')

code = '''
from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF

app = Flask(__name__)

# Load Data
resume_df = pd.read_excel("resume.xlsx")
jobs_df = pd.read_excel("jobs.xlsx")

jobs_df["job_text"] = jobs_df["job_title"].fillna('') + " " + jobs_df["job_description"].fillna('')
jobs_df_unique = jobs_df.drop_duplicates(subset=["job_title", "job_description"], keep='first').reset_index(drop=True)
job_texts = jobs_df_unique["job_text"].str.lower().str.strip().tolist()

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
job_vectors = vectorizer.fit_transform(job_texts)

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def rate_resume(score):
    if score >= 0.7:
        return "Excellent"
    elif score >= 0.5:
        return "Good"
    elif score >= 0.3:
        return "Average"
    else:
        return "Poor"

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        file = request.files['resume']
        filepath = "uploaded_resume.pdf"
        file.save(filepath)
        resume_text = extract_text_from_pdf(filepath)

        resume_vector = vectorizer.transform([resume_text])
        scores = cosine_similarity(resume_vector, job_vectors).flatten()

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

        for idx in top_matches:
            results.append({
                'title': jobs_df_unique.iloc[idx]['job_title'],
                'score': round(scores[idx], 2),
                'snippet': jobs_df_unique.iloc[idx]['job_description'][:150],
                'rating': rate_resume(scores[idx])
            })

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
'''
with open("app.py", "w") as f:
    f.write(code)

print("app.py created")

import os
os.makedirs("templates", exist_ok=True)

html_code = '''
<!doctype html>
<html>
<head>
    <title>Resume Matcher</title>
</head>
<body>
    <h1>Upload Your Resume</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="resume" required>
        <input type="submit" value="Match Jobs">
    </form>

    {% if results %}
        <h2>Top Matches:</h2>
        <ul>
            {% for match in results %}
                <li>
                    <strong>{{ match.title }}</strong><br>
                    Score: {{ match.score }}<br>
                    Rating: {{ match.rating }}<br>
                    Snippet: {{ match.snippet }}...
                </li><br>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
'''

with open("templates/index.html", "w") as f:
    f.write(html_code)

print("index.html created")

from google.colab import files
uploaded = files.upload()

reqs = '''
Flask
pandas
scikit-learn
PyMuPDF
'''
with open("requirements.txt", "w") as f:
    f.write(reqs.strip())

print("requirements.txt created")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

