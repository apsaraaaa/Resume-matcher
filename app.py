from flask import Flask, render_template, request
import fitz  # PyMuPDF
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load your job data
job_df = pd.read_excel("job_description.xlsx")

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    file = request.files['resume']
    resume_text = extract_text_from_pdf(file)

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([resume_text] + job_df['Job Description'].tolist())
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    best_match_index = cosine_similarities.argmax()

    best_job = job_df.iloc[best_match_index]
    return render_template('index.html',
                           job_title=best_job['Job Title'],
                           job_description=best_job['Job Description'],
                           score=round(cosine_similarities[best_match_index]*100, 2))

if __name__ == '__main__':
    app.run(debug=True)
