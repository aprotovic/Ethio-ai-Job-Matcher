# 🎯 AI Job Recommendation & Resume Matcher System

**An intelligent job matching platform built for the Ethiopian job market using Machine Learning and Natural Language Processing**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-orange)
![NLP](https://img.shields.io/badge/NLP-NLTK-green)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Datasets](#datasets)
- [Deployment](#deployment)
- [Limitations & Future Work](#limitations--future-work)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**AI Job Matcher Ethiopia** is a production-ready AI system that matches job seekers with relevant job opportunities based on their resumes. It uses advanced Natural Language Processing and Machine Learning techniques to:

- Analyze resume content and extract skills
- Match resumes with job descriptions
- Calculate similarity scores using TF-IDF and Cosine Similarity
- Rank jobs by relevance (0–100% match)
- Provide skill gap analysis and learning recommendations
- Optimize resumes for ATS (Applicant Tracking Systems)

Built specifically for the **Ethiopian job market** with datasets featuring Ethiopian companies, job titles, and local context.

---

## ✨ Features

### Core Features
- ✅ **Resume Upload** — Support for PDF, DOCX, and text input
- ✅ **AI-Powered Matching** — Uses TF-IDF vectorization and cosine similarity
- ✅ **Real-time Processing** — Get results in seconds
- ✅ **Match Percentage** — Clear 0–100% score for each job
- ✅ **Skill Extraction** — Automatically identifies technical and soft skills
- ✅ **Skill Gap Analysis** — Shows what skills you need to develop
- ✅ **Resume Optimizer (ATS)** — Scan your resume against a specific job for ATS compatibility
- ✅ **Visual Dashboard** — Interactive charts and analytics
- ✅ **Export Results** — Download matches as CSV

### Advanced Features
- 📊 **Analytics Dashboard** — Visualize match distributions
- 🎯 **Smart Filtering** — Filter by minimum match percentage
- 🏢 **Company Insights** — See top matching companies
- 📈 **Skill Trends** — Most in-demand skills in the market
- 🔍 **Detailed Job Cards** — Matched vs. missing skills breakdown

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Programming Language** | Python 3.8+ |
| **Machine Learning** | scikit-learn, NumPy |
| **NLP** | NLTK (Natural Language Toolkit) |
| **Web Framework** | Streamlit |
| **Data Processing** | Pandas |
| **Visualization** | Plotly |
| **File Processing** | PyPDF2, python-docx |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aprotovic/Ethio-ai-Job-Matcher.git
   cd Ethio-ai-Job-Matcher
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your default browser at `http://localhost:8501`

---

## 🚀 Usage

### Web Application

```bash
streamlit run app.py
```

Navigate through the sidebar:
- **🏠 Home** — Platform overview and quick-start guide
- **🎯 Job Matcher** — Upload your resume and get ranked job matches
- **📝 Resume Optimizer (ATS)** — Compare your resume to a specific job posting
- **📊 Analytics** — Visualize match score distributions and skill trends
- **ℹ️ About** — Technical details and project information
- **🚀 How It Works** — Deep dive into the ML pipeline

### Using the ML Engine Directly

```python
from ml_engine import JobMatcher, load_data

# Load data
resumes_df, jobs_df = load_data()

# Initialize matcher
matcher = JobMatcher()

# Match a resume with jobs
resume_text = "Your resume text here..."
results = matcher.match_resume_with_jobs(resume_text, jobs_df)

# Get top 5 recommendations
top_jobs = results.head(5)
print(top_jobs[['job_title', 'company', 'match_percentage']])
```

---

## 📁 Project Structure

```
Ethio-ai-Job-Matcher/
│
├── app.py                 # Streamlit web application
├── ml_engine.py           # Core ML algorithms and matching logic
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
├── README.md              # This file
├── QUICKSTART.md          # Quick setup guide
├── DEPLOYMENT.md          # Cloud deployment guide
│
└── data/
    ├── resumes.csv        # Sample resume dataset (20 resumes)
    └── jobs.csv           # Sample job dataset (20 jobs)
```

---

## 🧠 How It Works

### 1. Text Preprocessing
- Convert to lowercase
- Map technical terms (e.g. `c++` → `cpp`, `.net` → `dotnet`)
- Remove special characters and punctuation
- Tokenization (split into words)
- Remove stopwords (common words like "the", "is", "and")
- Lemmatization (convert words to base form: "running" → "run")

### 2. Feature Extraction (TF-IDF)

**TF-IDF** = Term Frequency × Inverse Document Frequency

- **TF**: How often a word appears in a document
- **IDF**: How rare/unique a word is across all documents
- Words that are important to specific documents get high scores

### 3. Similarity Calculation (Cosine Similarity)

```
similarity = cosine_similarity(resume_vector, job_vector)
# Result: 0.0 (no match) to 1.0 (perfect match)
```

Cosine similarity measures the angle between two vectors — it is independent of document length and is the industry standard for text similarity.

### 4. Ranking & Recommendations

1. Calculate similarity for all jobs
2. Convert to percentage (× 100)
3. Sort jobs by score (highest first)
4. Extract matched and missing skills
5. Return top N recommendations

---

## 📊 Datasets

### Resumes (`data/resumes.csv`)

**20 realistic Ethiopian resumes** covering roles such as Software Engineers, Data Scientists, Designers, HR Managers, and more.

### Jobs (`data/jobs.csv`)

**20 real job postings** from Ethiopian companies including:
- Kifiya Financial Technology, Ethio Telecom, Ethiopian Airlines
- Dashen Bank, Wegagen Bank, Awash Bank, Commercial Bank of Ethiopia
- Addis Software, iCog Labs, Gebeya Inc, and more

### Using Custom Datasets

You can replace the sample data with your own CSVs following the same column format:

```python
# Resumes: resume_id, resume_text
# Jobs: job_id, job_title, company, job_description
```

---

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides on deploying to:

- **Streamlit Cloud** (free)
- **Render**
- **Heroku**
- **Hugging Face Spaces**
- **AWS EC2**
- **Docker**

---

## ⚠️ Limitations & Future Work

### Current Limitations

1. **No Semantic Understanding** — Treats "Machine Learning" and "AI" as different terms
2. **Keyword Dependency** — Relies on exact word matches
3. **No User Feedback Loop** — Doesn't improve from user interactions
4. **No Personalization** — Same results for similar resumes

### Planned Improvements

- Replace TF-IDF with Word Embeddings (BERT / Sentence Transformers)
- Add Named Entity Recognition for better skill extraction
- Integrate user behavior signals (click-through rate, application rate)
- Multi-language support (Amharic, Oromiffa)
- Database backend (PostgreSQL) for production scale
- User authentication and saved profiles

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- [ ] Add more Ethiopian job datasets
- [ ] Implement Word2Vec/BERT embeddings
- [ ] Add multi-language support (Amharic, Oromiffa)
- [ ] Improve UI/UX design
- [ ] Add user authentication
- [ ] Create mobile app version

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ethiopian Tech Community** for inspiration
- **NLTK & scikit-learn** for excellent ML libraries
- **Streamlit** for the amazing web framework

---

## 📧 Contact & Support

- **GitHub**: [github.com/aprotovic/Ethio-ai-Job-Matcher](https://github.com/aprotovic/Ethio-ai-Job-Matcher)

---

**⭐ If you found this project helpful, please give it a star!**

**🇪🇹 Built with ❤️ for Ethiopian job seekers**
