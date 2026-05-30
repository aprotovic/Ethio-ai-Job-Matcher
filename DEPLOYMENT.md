# 🚀 Deployment Guide

Complete guide for deploying the AI Job Matcher System locally and on cloud platforms.

---

## 📋 Table of Contents

- [Local Deployment](#local-deployment)
- [Streamlit Cloud](#streamlit-cloud-free)
- [Render](#render)
- [Heroku](#heroku)
- [Hugging Face Spaces](#hugging-face-spaces)
- [AWS EC2](#aws-ec2)
- [Docker Deployment](#docker-deployment)
- [Production Best Practices](#production-best-practices)

---

## 💻 Local Deployment

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 500MB free disk space
- Internet connection (for NLTK downloads)

### Step-by-Step

1. **Clone the repository**
   ```bash
   git clone https://github.com/aprotovic/Ethio-ai-Job-Matcher.git
   cd Ethio-ai-Job-Matcher
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   streamlit run app.py
   ```

5. **Open Browser**
   - Navigate to: `http://localhost:8501`

### Troubleshooting Local Setup

**Issue: NLTK data not found**
```bash
python -c "import nltk; nltk.download('all')"
```

**Issue: Port already in use**
```bash
streamlit run app.py --server.port=8502
```

**Issue: Module not found**
```bash
pip install --upgrade -r requirements.txt
```

---

## ☁️ Streamlit Cloud (FREE)

**Best for**: Quick deployment, free hosting, easy updates

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   git remote add origin https://github.com/aprotovic/Ethio-ai-Job-Matcher.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `aprotovic/Ethio-ai-Job-Matcher`
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configuration (Optional)**
   Create `.streamlit/config.toml`:
   ```toml
   [theme]
   primaryColor = "#1E88E5"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F6"
   textColor = "#262730"
   font = "sans serif"

   [server]
   maxUploadSize = 10
   enableXsrfProtection = true
   ```

4. **Access Your App**
   - URL: `https://your-app-name.streamlit.app`
   - Custom domain available in settings

### Streamlit Cloud Features
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Auto-deployment on git push
- ✅ Built-in secrets management
- ✅ Easy rollback to previous versions

---

## 🎨 Render

**Best for**: Free tier, PostgreSQL support, flexible configuration

### Steps

1. **Create `render.yaml`**
   ```yaml
   services:
     - type: web
       name: ai-job-matcher-ethiopia
       env: python
       region: oregon
       plan: free
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
       envVars:
         - key: PYTHON_VERSION
           value: 3.10.0
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects configuration
   - Click "Create Web Service"

3. **Environment Variables (Optional)**
   ```
   STREAMLIT_SERVER_PORT=10000
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   STREAMLIT_SERVER_HEADLESS=true
   ```

4. **Access Your App**
   - URL: `https://your-app-name.onrender.com`

### Render Features
- ✅ Free tier (limited hours)
- ✅ Auto-deploy from GitHub
- ✅ Easy database integration
- ✅ Custom domains
- ✅ Health checks

---

## 🚀 Heroku

**Best for**: Quick deployment, extensive add-ons, scalability

### Setup Files

1. **Create `Procfile`**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create `setup.sh`**
   ```bash
   mkdir -p ~/.streamlit/

   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Create `runtime.txt`**
   ```
   python-3.10.12
   ```

### Deployment Steps

1. **Install Heroku CLI**
   ```bash
   # Mac
   brew tap heroku/brew && brew install heroku

   # Windows (download from heroku.com)
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create ai-job-matcher-ethiopia
   ```

3. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Heroku"
   heroku git:remote -a ai-job-matcher-ethiopia
   git push heroku main
   ```

4. **Open App**
   ```bash
   heroku open
   ```

### Heroku Management

```bash
# View logs
heroku logs --tail

# Scale dynos
heroku ps:scale web=1

# Set environment variables
heroku config:set MAX_UPLOAD_SIZE=10

# Restart app
heroku restart
```

---

## 🤗 Hugging Face Spaces

**Best for**: ML community, free GPU, easy sharing

### Steps

1. **Create Account**
   - Go to [huggingface.co](https://huggingface.co)
   - Sign up for free account

2. **Create New Space**
   - Click on profile → "Spaces"
   - Click "Create new Space"
   - Name: `ai-job-matcher-ethiopia`
   - License: MIT
   - SDK: **Streamlit**
   - Hardware: CPU (free)

3. **Upload Files**
   - Upload all project files via web interface
   - Or use git:
   ```bash
   git clone https://huggingface.co/spaces/aprotovic/Ethio-ai-Job-Matcher
   cd Ethio-ai-Job-Matcher
   # Copy your files here
   git add .
   git commit -m "Initial deployment"
   git push
   ```

4. **Access Your App**
   - URL: `https://huggingface.co/spaces/aprotovic/Ethio-ai-Job-Matcher`

### Hugging Face Features
- ✅ Free hosting
- ✅ Optional GPU/TPU
- ✅ ML community visibility
- ✅ Easy model integration
- ✅ Built-in CI/CD

---

## 🖥️ AWS EC2

**Best for**: Full control, production deployment, scalability

### Prerequisites
- AWS account
- SSH key pair
- Basic Linux knowledge

### Steps

1. **Launch EC2 Instance**
   ```
   Instance Type: t2.micro (free tier) or t2.medium
   OS: Ubuntu 22.04 LTS
   Storage: 20GB
   Security Group: Allow ports 22 (SSH) and 8501 (Streamlit)
   ```

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python
   sudo apt install python3-pip python3-venv -y

   # Install system dependencies
   sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
   ```

4. **Deploy Application**
   ```bash
   # Clone or upload project
   git clone https://github.com/aprotovic/Ethio-ai-Job-Matcher.git
   cd Ethio-ai-Job-Matcher

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install requirements
   pip install -r requirements.txt
   ```

5. **Run with systemd (Production)**

   Create `/etc/systemd/system/streamlit.service`:
   ```ini
   [Unit]
   Description=Streamlit AI Job Matcher
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/ai-job-matcher
   Environment="PATH=/home/ubuntu/ai-job-matcher/venv/bin"
   ExecStart=/home/ubuntu/ai-job-matcher/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0

   [Install]
   WantedBy=multi-user.target
   ```

   Enable service:
   ```bash
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   sudo systemctl status streamlit
   ```

6. **Configure Nginx (Optional)**
   ```bash
   sudo apt install nginx -y
   ```

   Create `/etc/nginx/sites-available/streamlit`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

---

## 🐳 Docker Deployment

**Best for**: Containerization, consistent environments, easy scaling

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t ai-job-matcher .

# Run container
docker run -p 8501:8501 ai-job-matcher

# Or use docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Push to Docker Hub

```bash
# Tag image
docker tag ai-job-matcher aprotovic/ai-job-matcher:latest

# Push to Docker Hub
docker push aprotovic/ai-job-matcher:latest
```

---

## 🏭 Production Best Practices

### 1. Environment Variables

Create `.env` file (never commit this):
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key
MAX_UPLOAD_SIZE=10
ENABLE_ANALYTICS=true
```

Load in application:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
```

### 2. Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### 3. Error Handling

```python
try:
    results = matcher.match_resume_with_jobs(resume_text, jobs_df)
except Exception as e:
    logger.error(f"Matching failed: {str(e)}", exc_info=True)
    st.error("An error occurred. Please try again.")
```

### 4. Database Integration

```python
import psycopg2

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Save match results
cur.execute("""
    INSERT INTO matches (user_id, job_id, score, timestamp)
    VALUES (%s, %s, %s, NOW())
""", (user_id, job_id, score))

conn.commit()
```

### 5. Caching

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_jobs():
    return pd.read_csv('data/jobs.csv')

@st.cache_resource
def load_model():
    return JobMatcher()
```

### 6. Monitoring

**Application Metrics:**
```python
import time

start_time = time.time()
results = matcher.match_resume_with_jobs(resume_text, jobs_df)
processing_time = time.time() - start_time

logger.info(f"Processing time: {processing_time:.2f}s")
```

**Health Check Endpoint:**
```python
# Add to app.py
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### 7. Security

```python
# Sanitize inputs
import re

def sanitize_text(text):
    # Remove potential XSS vectors
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    return text.strip()

# Rate limiting
from functools import lru_cache
import time

@st.cache_data(ttl=60)
def rate_limit_check(ip_address):
    # Implement rate limiting logic
    pass
```

### 8. Backup & Recovery

```bash
# Backup database
pg_dump -U postgres job_matcher > backup_$(date +%Y%m%d).sql

# Backup files
tar -czf backup_$(date +%Y%m%d).tar.gz data/ app.py ml_engine.py

# Restore
psql -U postgres job_matcher < backup_20241219.sql
```

---

## 📊 Performance Optimization

### 1. Code Optimization

```python
# Use vectorized operations
import numpy as np

# Instead of loops
scores = np.array([calculate_score(r, j) for r, j in zip(resumes, jobs)])

# Batch processing
def process_batch(resumes, jobs, batch_size=100):
    for i in range(0, len(resumes), batch_size):
        batch = resumes[i:i+batch_size]
        yield process_resumes(batch, jobs)
```

### 2. Database Indexing

```sql
CREATE INDEX idx_jobs_skills ON jobs USING GIN (skills);
CREATE INDEX idx_resumes_user_id ON resumes (user_id);
CREATE INDEX idx_matches_timestamp ON matches (timestamp DESC);
```

### 3. Load Balancing

Use Nginx for load balancing multiple instances:
```nginx
upstream streamlit_backend {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    location / {
        proxy_pass http://streamlit_backend;
    }
}
```

---

## 🔍 Monitoring & Analytics

### Google Analytics Integration

```python
# Add to app.py
import streamlit.components.v1 as components

# Google Analytics tracking
ga_code = """
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-XXXXX-Y"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-XXXXX-Y');
</script>
"""

components.html(ga_code)
```

---

## 📞 Support

For deployment issues:
- **GitHub Issues**: [github.com/aprotovic/Ethio-ai-Job-Matcher/issues](https://github.com/aprotovic/Ethio-ai-Job-Matcher/issues)

---

**Happy deploying! 🚀**
