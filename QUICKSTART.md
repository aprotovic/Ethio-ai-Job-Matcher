# 🚀 Quick Start Guide

Get the AI Job Matcher running in 5 minutes!

---

## ⚡ Super Quick Start

### Windows
```bash
git clone https://github.com/aprotovic/Ethio-ai-Job-Matcher.git
cd Ethio-ai-Job-Matcher
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Mac/Linux
```bash
git clone https://github.com/aprotovic/Ethio-ai-Job-Matcher.git
cd Ethio-ai-Job-Matcher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🎯 What to Expect

1. **First Run**: May take 1–2 minutes to download NLTK data
2. **Browser Opens**: Automatically opens at `http://localhost:8501`
3. **Upload Resume**: Click "Job Matcher" → Upload your resume
4. **Get Results**: See matched jobs in seconds!

---

## ❓ Troubleshooting

### "Python not found"
**Solution**: Install Python 3.8+ from [python.org](https://python.org)

### "pip not found"
**Solution**: 
```bash
# Windows
python -m ensurepip --upgrade

# Mac/Linux
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### "Port 8501 already in use"
**Solution**:
```bash
streamlit run app.py --server.port=8502
```

### "NLTK data not found"
**Solution**:
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

---

## 📝 Testing with Sample Data

The project includes 20 sample resumes and 20 jobs.

**Quick Test**:
1. Open `data/resumes.csv`
2. Copy any resume text
3. Go to the Job Matcher page
4. Paste the resume text
5. Click "Find Matching Jobs"

---

## 📧 Need Help?

- **GitHub Issues**: [github.com/aprotovic/Ethio-ai-Job-Matcher/issues](https://github.com/aprotovic/Ethio-ai-Job-Matcher/issues)
- **Documentation**: Check [README.md](README.md)

---

**Enjoy! 🎉**
