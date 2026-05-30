# 📊 Kaggle Dataset Integration Guide

How to use Kaggle datasets with this AI Job Matcher system.

---

## 🎯 Why Use Kaggle Datasets?

- **Larger Scale**: Thousands of real resumes and job postings
- **Real Data**: Actual job market data from companies
- **Diverse**: Multiple industries, roles, and experience levels
- **Free**: All datasets are free to download

---

## 🔧 Setup Kaggle

### 1. Install Kaggle CLI

```bash
pip install kaggle
```

### 2. Get API Credentials

1. Go to [kaggle.com](https://kaggle.com)
2. Sign in or create account
3. Go to Account settings
4. Scroll to "API" section
5. Click "Create New API Token"
6. Download `kaggle.json`

### 3. Configure Credentials

**Windows:**
```bash
mkdir %HOMEPATH%\.kaggle
move Downloads\kaggle.json %HOMEPATH%\.kaggle\
```

**Mac/Linux:**
```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

---

## 📦 Recommended Datasets

### 1. LinkedIn Job Postings (Best!)

**Dataset**: `promptcloud/linkedin-job-postings`  
**Size**: 1000+ jobs  
**Industries**: Tech, Finance, Healthcare, Sales

**Download:**
```bash
kaggle datasets download -d promptcloud/linkedin-job-postings
unzip linkedin-job-postings.zip -d data/kaggle/
```

**Integration:**
```python
import pandas as pd

# Load Kaggle data
linkedin_jobs = pd.read_csv('data/kaggle/linkedin-data-scientist-jobs.csv')

# Map to our format
jobs_df = pd.DataFrame({
    'job_id': range(len(linkedin_jobs)),
    'job_title': linkedin_jobs['position'],
    'company': linkedin_jobs['company'],
    'job_description': linkedin_jobs['job_summary']
})

# Save in our format
jobs_df.to_csv('data/jobs.csv', index=False)
```

---

### 2. Data Science Job Postings

**Dataset**: `ravindrasinghrana/job-description-dataset`  
**Size**: 19,000+ jobs  
**Focus**: Data Science, ML, AI roles

**Download:**
```bash
kaggle datasets download -d ravindrasinghrana/job-description-dataset
unzip job-description-dataset.zip -d data/kaggle/
```

**Integration:**
```python
jobs = pd.read_csv('data/kaggle/job_descriptions.csv')

jobs_df = pd.DataFrame({
    'job_id': range(len(jobs)),
    'job_title': jobs['Job Title'],
    'company': jobs['Company'],
    'job_description': jobs['Job Description']
})

jobs_df.to_csv('data/jobs.csv', index=False)
```

---

### 3. Resume Dataset

**Dataset**: `snehaanbhawal/resume-dataset`  
**Size**: 2,400+ resumes  
**Categories**: 25+ job categories

**Download:**
```bash
kaggle datasets download -d snehaanbhawal/resume-dataset
unzip resume-dataset.zip -d data/kaggle/
```

**Integration:**
```python
resumes = pd.read_csv('data/kaggle/Resume.csv')

resumes_df = pd.DataFrame({
    'resume_id': range(len(resumes)),
    'resume_text': resumes['Resume_str']  # or 'Resume_html' column
})

resumes_df.to_csv('data/resumes.csv', index=False)
```

---

### 4. Indeed Job Postings

**Dataset**: `madhab/jobposts`  
**Size**: 19,000+ jobs  
**Source**: Indeed.com

**Download:**
```bash
kaggle datasets download -d madhab/jobposts
unzip jobposts.zip -d data/kaggle/
```

---

### 5. Glassdoor Job Postings

**Dataset**: `rsadiq/glassdoor-job-postings`  
**Size**: 1000+ jobs  
**Features**: Salary, ratings, reviews

**Download:**
```bash
kaggle datasets download -d rsadiq/glassdoor-job-postings
unzip glassdoor-job-postings.zip -d data/kaggle/
```

---

## 🔄 Complete Integration Script

Create `integrate_kaggle.py`:

```python
"""
Script to integrate Kaggle datasets with AI Job Matcher
"""

import pandas as pd
import os

def integrate_linkedin_jobs():
    """Integrate LinkedIn job postings"""
    print("Loading LinkedIn jobs...")
    
    linkedin = pd.read_csv('data/kaggle/linkedin-job-postings.csv')
    
    jobs = pd.DataFrame({
        'job_id': range(1, len(linkedin) + 1),
        'job_title': linkedin['position'],
        'company': linkedin['company'],
        'job_description': linkedin['job_summary']
    })
    
    # Remove rows with missing data
    jobs = jobs.dropna()
    
    # Save
    jobs.to_csv('data/jobs_linkedin.csv', index=False)
    print(f"✓ Saved {len(jobs)} LinkedIn jobs")
    
    return jobs

def integrate_resume_dataset():
    """Integrate resume dataset"""
    print("Loading resumes...")
    
    resumes_raw = pd.read_csv('data/kaggle/Resume.csv')
    
    resumes = pd.DataFrame({
        'resume_id': range(1, len(resumes_raw) + 1),
        'resume_text': resumes_raw['Resume_str']
    })
    
    # Remove rows with missing data
    resumes = resumes.dropna()
    
    # Filter out very short resumes (< 100 chars)
    resumes = resumes[resumes['resume_text'].str.len() > 100]
    
    # Save
    resumes.to_csv('data/resumes_kaggle.csv', index=False)
    print(f"✓ Saved {len(resumes)} resumes")
    
    return resumes

def merge_with_existing(new_jobs, new_resumes):
    """Merge Kaggle data with existing Ethiopian data"""
    print("Merging datasets...")
    
    # Load existing
    existing_jobs = pd.read_csv('data/jobs.csv')
    existing_resumes = pd.read_csv('data/resumes.csv')
    
    # Merge
    all_jobs = pd.concat([existing_jobs, new_jobs], ignore_index=True)
    all_resumes = pd.concat([existing_resumes, new_resumes], ignore_index=True)
    
    # Reset IDs
    all_jobs['job_id'] = range(1, len(all_jobs) + 1)
    all_resumes['resume_id'] = range(1, len(all_resumes) + 1)
    
    # Save merged
    all_jobs.to_csv('data/jobs_merged.csv', index=False)
    all_resumes.to_csv('data/resumes_merged.csv', index=False)
    
    print(f"✓ Merged dataset: {len(all_jobs)} jobs, {len(all_resumes)} resumes")

def main():
    print("="*60)
    print("KAGGLE DATASET INTEGRATION")
    print("="*60)
    
    # Check if Kaggle data exists
    if not os.path.exists('data/kaggle/'):
        print("❌ Kaggle data not found!")
        print("Please download datasets first:")
        print("1. kaggle datasets download -d promptcloud/linkedin-job-postings")
        print("2. kaggle datasets download -d snehaanbhawal/resume-dataset")
        return
    
    # Integrate
    jobs = integrate_linkedin_jobs()
    resumes = integrate_resume_dataset()
    
    # Merge
    merge_with_existing(jobs, resumes)
    
    print("\n" + "="*60)
    print("✅ INTEGRATION COMPLETE!")
    print("="*60)
    print("\nNew files created:")
    print("- data/jobs_linkedin.csv")
    print("- data/resumes_kaggle.csv")
    print("- data/jobs_merged.csv")
    print("- data/resumes_merged.csv")
    print("\nUpdate ml_engine.py to use merged datasets:")
    print("resumes_df, jobs_df = load_data(")
    print("    resume_path='data/resumes_merged.csv',")
    print("    jobs_path='data/jobs_merged.csv'")
    print(")")

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python integrate_kaggle.py
```

---

## 📊 Data Quality Tips

### Cleaning Job Descriptions

```python
def clean_job_description(text):
    """Clean noisy job descriptions"""
    if pd.isna(text):
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove very long strings (likely garbage)
    words = text.split()
    words = [w for w in words if len(w) < 50]
    
    return ' '.join(words).strip()

jobs_df['job_description'] = jobs_df['job_description'].apply(clean_job_description)
```

### Filtering Relevant Jobs

```python
# Keep only jobs with substantial descriptions
jobs_df = jobs_df[jobs_df['job_description'].str.len() > 200]

# Filter by language (English only)
from langdetect import detect

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

jobs_df = jobs_df[jobs_df['job_description'].apply(is_english)]
```

---

## 🚀 Advanced: Combine Multiple Sources

```python
def load_multi_source_data():
    """Load data from multiple Kaggle datasets"""
    
    sources = [
        'data/kaggle/linkedin-jobs.csv',
        'data/kaggle/indeed-jobs.csv',
        'data/kaggle/glassdoor-jobs.csv'
    ]
    
    all_jobs = []
    
    for source in sources:
        if os.path.exists(source):
            df = pd.read_csv(source)
            # Standardize columns
            df = standardize_columns(df)
            all_jobs.append(df)
    
    # Combine
    combined = pd.concat(all_jobs, ignore_index=True)
    
    # Remove duplicates
    combined = combined.drop_duplicates(subset=['job_title', 'company'])
    
    return combined
```

---

## 📈 Performance with Large Datasets

### Sampling for Development

```python
# Use 10% sample for development
jobs_sample = jobs_df.sample(frac=0.1, random_state=42)
resumes_sample = resumes_df.sample(frac=0.1, random_state=42)
```

### Efficient Processing

```python
# Process in batches
def process_large_dataset(jobs_df, batch_size=1000):
    for i in range(0, len(jobs_df), batch_size):
        batch = jobs_df[i:i+batch_size]
        process_batch(batch)
```

---

## 🌍 Ethiopian Context Integration

Combine Kaggle international data with Ethiopian datasets:

```python
def add_ethiopian_context(jobs_df):
    """Add Ethiopian job market context"""
    
    # Load Ethiopian companies
    ethiopian_companies = [
        'Ethiopian Airlines', 'Ethio Telecom', 'Dashen Bank',
        'Safaricom Ethiopia', 'Kifiya Financial', 'iCog Labs'
    ]
    
    # Filter or tag Ethiopian jobs
    jobs_df['is_ethiopian'] = jobs_df['company'].isin(ethiopian_companies)
    
    # Prioritize Ethiopian jobs in results
    return jobs_df
```

---

## 🔍 Exploring Kaggle

**Search for datasets:**
```bash
kaggle datasets list -s "job"
kaggle datasets list -s "resume"
kaggle datasets list -s "career"
```

**Get dataset info:**
```bash
kaggle datasets files <dataset-name>
```

**Download specific files:**
```bash
kaggle datasets download <dataset-name> -f <filename>
```

---

## 📚 Additional Resources

- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Kaggle API Documentation](https://github.com/Kaggle/kaggle-api)
- [Data Cleaning Best Practices](https://towardsdatascience.com/data-cleaning-in-python)

---

**Happy Data Integration! 📊🚀**
