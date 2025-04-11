# 🌟 Resume-to-Job Matcher App 

## 🧠 What It Does

- 🧾 Upload a **PDF resume**
- 📚 Reads your resume using **PyMuPDF (fitz)**
- 🧠 Compares your skills & experience with job descriptions
- 📊 Shows your **top 3 job matches** with scores & match quality (Excellent/Good/Average/Poor)
- 🎯 Deploys as a web app using **Flask + Render**

---

## 🔍 Demo Preview

🌐 Live App Link:https://resume-matcher-rdrj.onrender.com
💻 **GitHub Repository:https://github.com/apsaraaaa/Resume-matcher.git

---

## 🛠️ Technologies Used

| Category        | Tech Stack                       |
|----------------|----------------------------------|
| Language        | Python                           |
| Libraries       | pandas, scikit-learn, fitz, Flask |
| Web Framework   | Flask                            |
| Visualization   | matplotlib, seaborn              |
| Deployment      | Render.com                       |
| Others          | TF-IDF, Cosine Similarity        |

---

## 📸 Screenshots

> ✨ *Visuals from analysis and final match results are available inside the project (bar plots + pie charts)*

---

## 📂 Folder Structure

resume-matcher/
├── app.py
├── job_aa_activity2.py
├── job_description.xlsx
├── resume.xlsx 
├── templates/
          └── index.html 
├── requirements.txt
          └── README.md


---

## 🚀 How to Run This Project Locally

```bash
git clone https://github.com/apsaraaaa/resume-matcher.git
cd resume-matcher
pip install -r requirements.txt
python app.py
