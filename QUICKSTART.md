# 🚀 Quick Start Guide

Get the AI Job Matcher running in 5 minutes!

---

## ⚡ Super Quick Start

### Windows
```bash
# 1. Extract the ZIP file
# 2. Open Command Prompt in the folder
# 3. Run these commands:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Mac/Linux
```bash
# 1. Extract the ZIP file
# 2. Open Terminal in the folder
# 3. Run these commands:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🎯 What to Expect

1. **First Run**: May take 1-2 minutes to download NLTK data
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
3. Go to Job Matcher page
4. Paste the resume text
5. Click "Find Matching Jobs"

---

## 🎓 Next Steps

1. **Read README.md** - Complete documentation
2. **Try Different Resumes** - Upload your own PDF/DOCX
3. **Explore Analytics** - Check the Analytics page
4. **Read Interview Guide** - Prepare for technical interviews
5. **Deploy Online** - See DEPLOYMENT.md

---

## 📧 Need Help?

- **Email**: support@aijobmatcher.et
- **Documentation**: Check README.md
- **Issues**: Check GitHub repository

---

**Enjoy! 🎉**
