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
- [Real-World Applications](#real-world-applications)
- [Limitations & Improvements](#limitations--improvements)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

This project is a **complete, production-ready AI system** that matches job seekers with relevant job opportunities based on their resumes. It uses advanced Natural Language Processing and Machine Learning techniques to:

- Analyze resume content and extract skills
- Match resumes with job descriptions
- Calculate similarity scores using TF-IDF and Cosine Similarity
- Rank jobs by relevance (0-100% match)
- Provide skill gap analysis and learning recommendations

**Built specifically for the Ethiopian job market** with sample datasets featuring Ethiopian companies, job titles, and local context.

---

## ✨ Features

### Core Features
- ✅ **Resume Upload** - Support for PDF, DOCX, and text input
- ✅ **AI-Powered Matching** - Uses TF-IDF vectorization and cosine similarity
- ✅ **Real-time Processing** - Get results in seconds
- ✅ **Match Percentage** - Clear 0-100% score for each job
- ✅ **Skill Extraction** - Automatically identifies technical and soft skills
- ✅ **Skill Gap Analysis** - Shows what skills you need to learn
- ✅ **Visual Dashboard** - Interactive charts and analytics
- ✅ **Export Results** - Download matches as CSV

### Advanced Features
- 📊 **Analytics Dashboard** - Visualize match distributions
- 🎯 **Smart Filtering** - Filter by minimum match percentage
- 🏢 **Company Insights** - See top matching companies
- 📈 **Skill Trends** - Most in-demand skills in the market
- 🔍 **Detailed Job Cards** - Matched vs missing skills breakdown

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
- 500MB free disk space

### Step-by-Step Installation

1. **Download and Extract the Project**
   ```bash
   # Extract the ZIP file to your desired location
   unzip ai-job-matcher-ethiopia.zip
   cd ai-job-matcher-ethiopia
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK Data**
   ```python
   # This happens automatically on first run, but you can do it manually:
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
   ```

---

## 🚀 Usage

### Running the Web Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

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

### Testing the ML Engine

```bash
python ml_engine.py
```

This will run a test with sample data and display results in the terminal.

---

## 📁 Project Structure

```
ai-job-matcher-ethiopia/
│
├── app.py                      # Main Streamlit web application
├── ml_engine.py               # Core ML algorithms and matching logic
├── requirements.txt           # Python dependencies
│
├── data/                      # Dataset directory
│   ├── resumes.csv           # Sample resume data (20 resumes)
│   └── jobs.csv              # Sample job data (20 jobs)
│
├── docs/                      # Documentation
│   ├── DEPLOYMENT.md         # Deployment guide
│   ├── INTERVIEW_GUIDE.md    # Interview preparation
│   └── TECHNICAL_DEEP_DIVE.md # Technical explanation
│
├── tests/                     # Test files
│   └── test_ml_engine.py     # Unit tests
│
└── README.md                  # This file
```

---

## 🧠 How It Works

### 1. Text Preprocessing
```python
# Steps performed on both resume and job descriptions:
1. Convert to lowercase
2. Remove special characters and punctuation
3. Tokenization (split into words)
4. Remove stopwords (common words like "the", "is", "and")
5. Lemmatization (convert words to base form: "running" → "run")
```

### 2. Feature Extraction (TF-IDF)

**TF-IDF** = Term Frequency × Inverse Document Frequency

- **TF**: How often a word appears in a document
- **IDF**: How rare/unique a word is across all documents
- **Result**: Words that are important to specific documents get high scores

Example:
- "Python" in a developer resume: High TF-IDF (important skill)
- "experience" in any resume: Low TF-IDF (common word)

### 3. Similarity Calculation (Cosine Similarity)

```python
similarity = cosine_similarity(resume_vector, job_vector)
# Result: 0.0 (no match) to 1.0 (perfect match)
```

**Why Cosine Similarity?**
- Measures angle between vectors, not distance
- Independent of document length
- Perfect for text similarity

### 4. Ranking & Recommendations

```python
1. Calculate similarity for all jobs
2. Convert to percentage (× 100)
3. Sort jobs by score (highest first)
4. Extract matched and missing skills
5. Return top N recommendations
```

---

## 📊 Datasets

### Resumes Dataset (`data/resumes.csv`)

**20 realistic Ethiopian resumes** featuring:
- Software Engineers, Data Scientists, Full Stack Developers
- Digital Marketers, Network Engineers, Graphic Designers
- Mechanical Engineers, HR Managers, Mobile App Developers
- Content Writers, Accountants, Civil Engineers
- AI/ML Engineers, Cybersecurity Analysts, Business Analysts
- DevOps Engineers, UX/UI Designers, Sales Managers
- Nurses, Electrical Engineers

**Columns:**
- `resume_id`: Unique identifier
- `resume_text`: Full resume content with skills, experience, education

### Jobs Dataset (`data/jobs.csv`)

**20 real job postings** from Ethiopian companies:
- Kifiya Financial Technology, Ethio Telecom, Ethiopian Airlines
- Dashen Bank, Wegagen Bank, Awash Bank, Commercial Bank of Ethiopia
- Addis Software, iCog Labs, Gebeya Inc, Ride Ethiopia
- Zemen Design Studio, M-Birr, China State Construction
- Reppie Waste-to-Energy Plant, Solar Energy Foundation

**Columns:**
- `job_id`: Unique identifier
- `job_title`: Position name
- `company`: Company name
- `job_description`: Full job description with requirements

### Using Custom Datasets

You can easily use your own data:

```python
# Create your own CSV files following the same format
# Or use Kaggle datasets:

# Popular job datasets on Kaggle:
# 1. "Job Postings on Glassdoor"
# 2. "LinkedIn Job Postings"
# 3. "Data Scientist Job Market in the U.S."

# Load custom data
custom_resumes = pd.read_csv('your_resumes.csv')
custom_jobs = pd.read_csv('your_jobs.csv')
```

**Kaggle Integration:**
```bash
pip install kaggle

# Download a dataset
kaggle datasets download -d promptcloud/linkedin-job-postings

# Unzip and use
unzip linkedin-job-postings.zip -d data/
```

---

## 🌐 Deployment

### Local Deployment
Already covered in [Usage](#usage) section.

### Cloud Deployment

#### 1. Streamlit Cloud (Free & Easy)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_URL
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

Your app will be live at: `https://your-app-name.streamlit.app`

#### 2. Render (Free Tier Available)

Create `render.yaml`:
```yaml
services:
  - type: web
    name: ai-job-matcher
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT
```

Deploy:
1. Connect GitHub repo to Render
2. Select "Web Service"
3. Follow deployment steps

#### 3. Heroku

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]" > ~/.streamlit/config.toml
echo "headless = true" >> ~/.streamlit/config.toml
echo "port = $PORT" >> ~/.streamlit/config.toml
```

Deploy:
```bash
heroku login
heroku create ai-job-matcher-ethiopia
git push heroku main
```

#### 4. Hugging Face Spaces

1. Create new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select "Streamlit" SDK
3. Upload your files
4. Done!

---

## 🏢 Real-World Applications

### How Companies Use This Technology

#### LinkedIn
- **Use Case**: "Jobs you may be interested in"
- **Scale**: Matches millions of resumes daily
- **Improvements**: Deep learning models, user behavior signals
- **Tech**: Embeddings (Word2Vec, BERT), neural networks

#### Indeed
- **Use Case**: Resume-job matching for employers
- **Scale**: 250M+ resumes, 10M+ jobs
- **Improvements**: Location-based filtering, salary matching
- **Tech**: Multi-stage ranking, personalization

#### Glassdoor
- **Use Case**: Career insights and job recommendations
- **Scale**: 100M+ users
- **Improvements**: Company culture fit, interview difficulty
- **Tech**: Hybrid recommendation systems

#### Recruitment Agencies
- **Use Case**: Automated candidate screening
- **Scale**: Thousands of applications per position
- **Improvements**: Video interview analysis, soft skill assessment
- **Tech**: NLP + Computer Vision

### Scaling to Millions of Users

**Infrastructure Requirements:**

```
┌─────────────┐
│   Users     │
└──────┬──────┘
       │
┌──────▼──────────┐
│ Load Balancer   │ (AWS ELB, Nginx)
└──────┬──────────┘
       │
┌──────▼──────────┐
│  API Servers    │ (Flask/FastAPI, multiple instances)
└──────┬──────────┘
       │
┌──────▼──────────┐
│  ML Service     │ (Dedicated GPU/CPU workers)
└──────┬──────────┘
       │
┌──────▼──────────┬──────────────┬──────────────┐
│   Database      │    Cache     │    Queue     │
│  (PostgreSQL)   │   (Redis)    │ (RabbitMQ)   │
└─────────────────┴──────────────┴──────────────┘
```

**Technologies:**
- **Database**: PostgreSQL (structured data), MongoDB (document store)
- **Cache**: Redis (fast key-value store)
- **Search**: Elasticsearch (full-text search)
- **Queue**: RabbitMQ/Kafka (async processing)
- **Cloud**: AWS (EC2, S3, RDS) or Azure
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

---

## ⚠️ Limitations & Improvements

### Current Limitations

1. **No Semantic Understanding**
   - Treats "Machine Learning" and "AI" as different terms
   - Misses synonyms and related concepts

2. **Keyword Dependency**
   - Relies heavily on exact word matches
   - Can be gamed by keyword stuffing

3. **No Learning Capability**
   - Doesn't improve from user feedback
   - Static model weights

4. **Limited Context**
   - Doesn't understand job market trends
   - No temporal awareness

5. **No Personalization**
   - Same results for similar resumes
   - No user preference learning

### Recommended Improvements

#### 1. Use Word Embeddings (Intermediate)

```python
from sentence_transformers import SentenceTransformer

# Replace TF-IDF with BERT embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

resume_embedding = model.encode(resume_text)
job_embeddings = model.encode(job_descriptions)

# Calculate similarity
similarities = cosine_similarity([resume_embedding], job_embeddings)
```

**Benefits:**
- Understands semantic meaning
- "Machine Learning" matches with "AI" and "Deep Learning"
- Better handling of context

#### 2. Deep Learning Models (Advanced)

```python
import tensorflow as tf

# Two-tower neural network
resume_tower = create_neural_network(resume_features)
job_tower = create_neural_network(job_features)

# Learn similarity from historical data
similarity = dot_product(resume_tower, job_tower)
```

**Benefits:**
- Learns from historical matches
- Personalized recommendations
- Multi-modal inputs (text, structured data)

#### 3. Add User Behavior Signals

```python
# Features to include:
- Click-through rate (CTR)
- Application completion rate
- Time spent on job page
- User feedback (likes/dislikes)
- Past job applications
```

**Benefits:**
- Personalized results
- Learns user preferences
- Improves over time

#### 4. Named Entity Recognition (NER)

```python
import spacy

nlp = spacy.load('en_core_web_sm')

# Extract entities
doc = nlp(resume_text)
companies = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']
```

**Benefits:**
- Better skill extraction
- Company experience matching
- Education level comparison

#### 5. A/B Testing Framework

```python
# Test different algorithms
if user_id % 2 == 0:
    results = tfidf_matcher(resume, jobs)
else:
    results = embedding_matcher(resume, jobs)

# Track which performs better
log_metrics(algorithm, user_interactions)
```

---

## 💼 Interview Preparation Guide

### Common Interview Questions

**Q1: Why did you choose TF-IDF over other methods?**

**A:** TF-IDF is a good baseline for text similarity because:
- Simple to implement and interpret
- Fast computation (important for real-time systems)
- Proven effectiveness for keyword-based matching
- Low computational requirements
- Good for sparse, high-dimensional data

However, for production systems, I'd recommend Word2Vec or BERT for better semantic understanding.

---

**Q2: How would you handle spelling mistakes in resumes?**

**A:** Several approaches:
1. **Fuzzy Matching**: Use Levenshtein distance to find similar words
2. **Spell Checkers**: Libraries like `pyspellchecker` or `textblob`
3. **N-gram Matching**: Match character sequences
4. **Deep Learning**: Train a seq2seq model for correction

Example:
```python
from textblob import TextBlob

def correct_spelling(text):
    return str(TextBlob(text).correct())
```

---

**Q3: How do you prevent bias in job matching?**

**A:** Important considerations:
1. **Remove Protected Attributes**: Don't use gender, age, race in matching
2. **Fairness Constraints**: Ensure equal opportunity across groups
3. **Bias Audits**: Regularly test for disparate impact
4. **Diverse Training Data**: Include varied backgrounds
5. **Explainability**: Make matching criteria transparent

---

**Q4: How would you evaluate your system's performance?**

**A:** Multiple metrics:
1. **Precision@K**: How many of top K recommendations are relevant
2. **Recall@K**: How many relevant jobs are in top K
3. **MAP**: Mean Average Precision across all users
4. **User Engagement**: Click-through rate, application rate
5. **Business Metrics**: Time-to-hire, quality of hire
6. **A/B Testing**: Compare against baseline system

---

**Q5: How would you scale this for 1 million concurrent users?**

**A:** Architecture improvements:
1. **Horizontal Scaling**: Multiple API servers behind load balancer
2. **Caching**: Redis for frequently accessed data
3. **Async Processing**: Queue system for heavy computations
4. **Database Optimization**: Indexing, read replicas
5. **CDN**: Cache static assets
6. **Microservices**: Separate services for different functions
7. **Auto-scaling**: Based on load metrics

---

**Q6: What are the limitations of cosine similarity?**

**A:** Limitations:
1. **No semantic understanding**: "Car" and "Automobile" are treated as different
2. **Sensitive to vocabulary**: Different words for same concept
3. **Sparse vectors**: Most TF-IDF dimensions are zero
4. **Context-agnostic**: "Apple" (fruit) vs "Apple" (company)

**Solutions:**
- Use embeddings (Word2Vec, BERT)
- Combine with other features
- Add domain knowledge

---

**Q7: How would you handle multi-language support (Amharic, Oromiffa)?**

**A:** Approaches:
1. **Translation**: Translate all text to English first
2. **Multi-lingual Models**: Use XLM-RoBERTa or mBERT
3. **Language-Specific Models**: Train separate models per language
4. **Cross-lingual Embeddings**: Map languages to same vector space

For Ethiopian languages:
```python
# Use Google Translate API
from googletrans import Translator

translator = Translator()
english_text = translator.translate(amharic_text, src='am', dest='en').text
```

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
- [ ] Implement email notifications
- [ ] Create mobile app version
- [ ] Add more visualization options

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ethiopian Tech Community** for inspiration
- **NLTK & scikit-learn** for excellent ML libraries
- **Streamlit** for the amazing web framework
- **All contributors** who helped improve this project

---

## 📧 Contact & Support

- **Email**: info@aijobmatcher.et
- **Website**: www.aijobmatcher.et
- **GitHub**: github.com/ai-job-matcher-ethiopia
- **LinkedIn**: linkedin.com/company/ai-job-matcher

---

**⭐ If you found this project helpful, please give it a star!**

**🇪🇹 Built with ❤️ for Ethiopian job seekers**

---

## 📚 Additional Resources

### Learning Resources
- [Natural Language Processing with Python](https://www.nltk.org/book/)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [TF-IDF Explained](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)

### Similar Projects
- [LinkedIn Talent Hub](https://business.linkedin.com/talent-solutions/talent-hub)
- [Indeed Resume Search](https://www.indeed.com/hire/resume-search)
- [JobScan ATS Optimization](https://www.jobscan.co/)

### Ethiopian Tech Community
- [IceAddis](https://iceaddis.com/)
- [Gebeya](https://gebeya.com/)
- [iCog Labs](https://icog-labs.com/)
- [Ethiopian Artificial Intelligence Institute](https://www.aai.et/)

---

**Last Updated**: December 2024
