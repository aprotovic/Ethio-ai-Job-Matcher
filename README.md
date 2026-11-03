# 🎯 Ethio AI Job Matcher & Resume Parser

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![NLP](https://img.shields.io/badge/NLP-NLTK%20%7C%20TF--IDF-green.svg)](https://www.nltk.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, AI-powered career recommendation engine and resume parser built specifically for the Ethiopian job market. Matches candidate CVs against enterprise vacancy postings with real-time match scoring and skill gap insights.

---

## ✨ Key Features

- **Document Parsing:** Ingests PDF, DOCX, and raw text resumes using OCR and text extractors.
- **NLP Matching Engine:** Preprocesses text with NLTK and calculates Cosine Similarity across TF-IDF vector embeddings.
- **Ethiopian Enterprise Dataset:** Pre-configured with actual vacancy postings from Ethio Telecom, Ethiopian Airlines, Dashen Bank, Commercial Bank of Ethiopia (CBE), etc.
- **ATS Resume Optimizer:** Pinpoints missing keywords and provides concrete recommendations to increase interview callback rates.
- **Interactive Visualizations:** Match distributions and skill frequency analytics powered by Plotly.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **AI / NLP** | Scikit-Learn, NLTK (Tokenization, Lemmatization), TF-IDF Vectorizer |
| **Frontend UI** | Streamlit, Plotly Express |
| **File Processing** | PyPDF2, python-docx, Pandas |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/aprotovic/Ethio-ai-Job-Matcher.git
cd Ethio-ai-Job-Matcher

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the web application
streamlit run app.py
```
Open **http://localhost:8501** in your browser.

---

## 📄 License
Distributed under the MIT License. Built with ❤️ by [aprotovic](https://github.com/aprotovic).
