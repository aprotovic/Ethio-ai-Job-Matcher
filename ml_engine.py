"""
AI Job Recommendation & Resume Matcher System
Machine Learning Engine

This module handles all ML operations:
- Text preprocessing (NLP)
- Feature extraction (TF-IDF)
- Similarity calculation (Cosine Similarity)
- Job ranking and recommendations
"""

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


class JobMatcher:
    """
    Main class for AI-powered job matching system
    Uses NLP and Machine Learning for resume-job matching
    """
    
    def __init__(self):
        """Initialize the JobMatcher with necessary NLP tools"""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),  # Use unigrams and bigrams
            min_df=1,
            stop_words='english'
        )
        self.lemmatizer = WordNetLemmatizer()
        
        # Fallback list of English stopwords in case NLTK is not available
        self.fallback_stopwords = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
            'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
            'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
            'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
            'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
            "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
            'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
            'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
            'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
        }
        
        # Download required NLTK data with graceful fallbacks
        self.nltk_stopwords_available = True
        self.nltk_tokenizers_available = True
        self.nltk_wordnet_available = True
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            try:
                nltk.download('stopwords', quiet=True)
            except Exception:
                self.nltk_stopwords_available = False
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
            except Exception:
                self.nltk_tokenizers_available = False
            
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            try:
                nltk.download('wordnet', quiet=True)
            except Exception:
                self.nltk_wordnet_available = False
    
    
    def preprocess_text(self, text):
        """
        Comprehensive text preprocessing pipeline
        
        Steps:
        1. Convert to lowercase
        2. Map technical terms (e.g., c++ -> cpp)
        3. Remove special characters and punctuation
        4. Tokenization (with fallback)
        5. Remove stopwords (with fallback)
        6. Lemmatization (with fallback)
        
        Args:
            text (str): Raw text input
            
        Returns:
            str: Cleaned and preprocessed text
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        # Convert to lowercase
        text = text.lower()
        
        # Map key technical terms before removing special characters
        tech_map = {
            r'\bc\+\+(?![a-zA-Z0-9])': 'cpp',
            r'\bc#(?![a-zA-Z0-9])': 'csharp',
            r'(?<![a-zA-Z0-9])\.net\b': 'dotnet',
            r'\bnode\.js\b': 'nodejs',
            r'\breact\.js\b': 'reactjs',
            r'\bvue\.js\b': 'vuejs',
            r'\bd3\.js\b': 'd3js',
            r'\bui/ux\b': 'uiux',
            r'\bci/cd\b': 'cicd'
        }
        for pattern, replacement in tech_map.items():
            text = re.sub(pattern, replacement, text)
        
        # Remove special characters, keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenization (with fallback if NLTK data is not loaded)
        if self.nltk_tokenizers_available:
            try:
                tokens = word_tokenize(text)
            except Exception:
                tokens = [w for w in re.split(r'\W+', text) if w]
        else:
            tokens = [w for w in re.split(r'\W+', text) if w]
        
        # Remove stopwords (with fallback if NLTK data is not loaded)
        if self.nltk_stopwords_available:
            try:
                stop_words = set(stopwords.words('english'))
            except Exception:
                stop_words = self.fallback_stopwords
        else:
            stop_words = self.fallback_stopwords
            
        tokens = [word for word in tokens if word not in stop_words]
        
        # Lemmatization (convert words to base form, with fallback)
        if self.nltk_wordnet_available:
            try:
                tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
            except Exception:
                pass
        
        # Join tokens back into string
        cleaned_text = ' '.join(tokens)
        
        return cleaned_text
    
    
    def extract_skills(self, text, skill_keywords=None):
        """
        Extract skills from text based on predefined skill keywords.
        Uses boundary assertions to prevent substring collision matching
        (e.g. 'java' matching 'javascript' or 'api' matching 'rapid').
        
        Args:
            text (str): Text to extract skills from
            skill_keywords (list): List of skill keywords to search for
            
        Returns:
            list: List of found skills
        """
        if not isinstance(text, str) or not text.strip():
            return []

        if skill_keywords is None:
            # Common tech and professional skills
            skill_keywords = [
                'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
                'django', 'flask', 'spring', 'express', 'mongodb', 'mysql', 'postgresql',
                'sql', 'nosql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
                'machine learning', 'deep learning', 'ai', 'nlp', 'tensorflow', 'pytorch',
                'scikit-learn', 'data analysis', 'data science', 'statistics',
                'html', 'css', 'bootstrap', 'tailwind', 'git', 'github', 'gitlab',
                'agile', 'scrum', 'devops', 'ci/cd', 'jenkins', 'linux', 'bash',
                'api', 'rest', 'graphql', 'microservices', 'cloud', 'security',
                'testing', 'junit', 'selenium', 'cypress', 'jest',
                'marketing', 'seo', 'sem', 'social media', 'content marketing',
                'google analytics', 'adobe', 'photoshop', 'illustrator', 'figma',
                'ui/ux', 'design', 'autocad', 'solidworks', 'revit',
                'project management', 'leadership', 'communication', 'teamwork',
                'networking', 'cisco', 'ccna', 'firewall', 'vpn',
                'accounting', 'finance', 'excel', 'quickbooks', 'sap', 'erp',
                'hr', 'recruitment', 'payroll', 'labor law', 'c++', 'c#', '.net'
            ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            # Construct a regex matching the skill as a whole word or phrase,
            # ensuring it is not preceded or followed by alphanumeric characters.
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill.lower()) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    
    def vectorize_texts(self, texts):
        """
        Convert texts to TF-IDF vectors
        
        TF-IDF (Term Frequency-Inverse Document Frequency):
        - Measures importance of words in documents
        - Higher score = more important word for that document
        
        Args:
            texts (list): List of text documents
            
        Returns:
            array: TF-IDF matrix
        """
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        return tfidf_matrix
    
    
    def calculate_similarity(self, resume_vector, job_vectors):
        """
        Calculate cosine similarity between resume and jobs
        
        Cosine Similarity:
        - Measures angle between two vectors
        - Range: 0 (no similarity) to 1 (identical)
        - Perfect for text similarity
        
        Args:
            resume_vector: TF-IDF vector of resume
            job_vectors: TF-IDF vectors of job descriptions
            
        Returns:
            array: Similarity scores
        """
        similarities = cosine_similarity(resume_vector, job_vectors)
        return similarities[0]  # Return 1D array
    
    
    def match_resume_with_jobs(self, resume_text, jobs_df):
        """
        Main matching function - matches resume with all jobs
        
        Process:
        1. Preprocess resume and job descriptions
        2. Vectorize using TF-IDF
        3. Calculate cosine similarity
        4. Rank jobs by similarity
        5. Extract matched skills
        
        Args:
            resume_text (str): User's resume text
            jobs_df (DataFrame): DataFrame containing job descriptions
            
        Returns:
            DataFrame: Ranked job recommendations with match scores
        """
        # Defensive check for empty inputs
        if jobs_df.empty or not resume_text.strip():
            return pd.DataFrame(columns=[
                'job_id', 'job_title', 'company', 'job_description',
                'match_percentage', 'matched_skills', 'missing_skills'
            ])

        # Preprocess resume
        print("🔄 Preprocessing resume...")
        cleaned_resume = self.preprocess_text(resume_text)
        
        # Preprocess all job descriptions
        print("🔄 Preprocessing job descriptions...")
        jobs_df = jobs_df.copy()
        jobs_df['cleaned_description'] = jobs_df['job_description'].apply(
            self.preprocess_text
        )
        
        # Combine resume and jobs for vectorization
        all_texts = [cleaned_resume] + jobs_df['cleaned_description'].tolist()
        
        # Vectorize using TF-IDF
        print("🔄 Extracting features using TF-IDF...")
        tfidf_matrix = self.vectorize_texts(all_texts)
        
        # Separate resume vector from job vectors
        resume_vector = tfidf_matrix[0:1]
        job_vectors = tfidf_matrix[1:]
        
        # Calculate similarity scores
        print("🔄 Calculating similarity scores...")
        similarity_scores = self.calculate_similarity(resume_vector, job_vectors)
        
        # Add scores to dataframe
        jobs_df['match_score'] = similarity_scores
        jobs_df['match_percentage'] = (similarity_scores * 100).round(2)
        
        # Extract skills from resume
        resume_skills = self.extract_skills(resume_text)
        
        # Extract skills from each job
        jobs_df['required_skills'] = jobs_df['job_description'].apply(
            self.extract_skills
        )
        
        # Find matched and missing skills
        jobs_df['matched_skills'] = jobs_df['required_skills'].apply(
            lambda job_skills: list(set(job_skills) & set(resume_skills))
        )
        
        jobs_df['missing_skills'] = jobs_df['required_skills'].apply(
            lambda job_skills: list(set(job_skills) - set(resume_skills))
        )
        
        # Sort by match score (highest first)
        jobs_df = jobs_df.sort_values('match_score', ascending=False).reset_index(drop=True)
        
        print("✅ Matching complete!")
        
        # Return relevant columns
        result_df = jobs_df[[
            'job_id', 'job_title', 'company', 'job_description',
            'match_percentage', 'matched_skills', 'missing_skills'
        ]]
        
        return result_df
    
    
    def get_top_recommendations(self, matched_jobs_df, top_n=5):
        """
        Get top N job recommendations
        
        Args:
            matched_jobs_df (DataFrame): DataFrame with matched jobs
            top_n (int): Number of top jobs to return
            
        Returns:
            DataFrame: Top N jobs
        """
        return matched_jobs_df.head(top_n)
    
    
    def analyze_skill_gap(self, resume_text, top_jobs_df):
        """
        Analyze skill gaps based on top job matches
        
        Args:
            resume_text (str): User's resume
            top_jobs_df (DataFrame): Top matched jobs
            
        Returns:
            dict: Skill gap analysis
        """
        resume_skills = set(self.extract_skills(resume_text))
        
        if top_jobs_df.empty:
            return {
                'current_skills_count': len(resume_skills),
                'current_skills': list(resume_skills),
                'top_missing_skills': [],
                'skill_gap_details': []
            }

        # Collect all required skills from top jobs
        all_required_skills = set()
        for skills in top_jobs_df['missing_skills']:
            all_required_skills.update(skills)
        
        # Count frequency of missing skills
        skill_frequency = {}
        for skills in top_jobs_df['missing_skills']:
            for skill in skills:
                skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        # Sort by frequency
        top_missing_skills = sorted(
            skill_frequency.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        analysis = {
            'current_skills_count': len(resume_skills),
            'current_skills': list(resume_skills),
            'top_missing_skills': [skill for skill, _ in top_missing_skills],
            'skill_gap_details': top_missing_skills
        }
        
        return analysis


def load_data(resume_path='data/resumes.csv', jobs_path='data/jobs.csv'):
    """
    Load resume and job datasets
    
    Args:
        resume_path (str): Path to resumes CSV
        jobs_path (str): Path to jobs CSV
        
    Returns:
        tuple: (resumes_df, jobs_df)
    """
    resumes_df = pd.read_csv(resume_path)
    jobs_df = pd.read_csv(jobs_path)
    return resumes_df, jobs_df


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("AI JOB RECOMMENDATION & RESUME MATCHER SYSTEM")
    print("Machine Learning Engine Test")
    print("="*60)
    
    # Load data
    resumes_df, jobs_df = load_data()
    
    # Initialize matcher
    matcher = JobMatcher()
    
    # Test with first resume
    test_resume = resumes_df.iloc[0]['resume_text']
    print(f"\nTesting with resume: {test_resume[:100]}...")
    
    # Match resume with jobs
    results = matcher.match_resume_with_jobs(test_resume, jobs_df.copy())
    
    # Show top 5 recommendations
    print("\n" + "="*60)
    print("TOP 5 JOB RECOMMENDATIONS")
    print("="*60)
    
    top_5 = results.head(5)
    for idx, row in top_5.iterrows():
        print(f"\n{idx+1}. {row['job_title']} at {row['company']}")
        print(f"   Match: {row['match_percentage']}%")
        print(f"   Matched Skills: {', '.join(row['matched_skills'][:5]) if row['matched_skills'] else 'None'}")
        print(f"   Missing Skills: {', '.join(row['missing_skills'][:3]) if row['missing_skills'] else 'None'}")
    
    # Skill gap analysis
    print("\n" + "="*60)
    print("SKILL GAP ANALYSIS")
    print("="*60)
    
    skill_analysis = matcher.analyze_skill_gap(test_resume, top_5)
    print(f"\nCurrent Skills: {skill_analysis['current_skills_count']}")
    print(f"Top Skills to Learn: {', '.join(skill_analysis['top_missing_skills'][:5])}")
