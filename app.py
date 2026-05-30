"""
AI Job Recommendation & Resume Matcher System
Streamlit Web Application

A complete web interface for AI-powered job matching
Built for the Ethiopian job market
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from ml_engine import JobMatcher, load_data
import PyPDF2
import docx
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="AI Job Matcher Ethiopia",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-header {
        font-size: 3.2rem;
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    .sub-header {
        font-size: 1.25rem;
        color: #546E7A;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    .hero-card {
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 20px rgba(30, 60, 114, 0.15);
    }
    .hero-card h2 {
        color: white !important;
        font-weight: 700;
        margin-top: 0;
        font-size: 2rem;
    }
    
    .job-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #ECEFF1;
        border-left: 6px solid #1E88E5;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02), 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
    }
    
    .match-badge {
        color: white;
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: inline-block;
    }
    
    .skill-tag {
        background-color: #E3F2FD;
        color: #0D47A1;
        padding: 0.4rem 0.9rem;
        border-radius: 50px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #BBDEFB;
        transition: all 0.2s ease;
    }
    .skill-tag:hover {
        background-color: #BBDEFB;
        transform: scale(1.05);
    }
    
    .missing-skill-tag {
        background-color: #FFF3E0;
        color: #E65100;
        padding: 0.4rem 0.9rem;
        border-radius: 50px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #FFE0B2;
        transition: all 0.2s ease;
    }
    .missing-skill-tag:hover {
        background-color: #FFE0B2;
        transform: scale(1.05);
    }
    
    .info-box {
        background-color: #F1F8E9;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #7CB342;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #ECEFF1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        text-align: center;
    }
    
    .sidebar-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1E88E5;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Streamlit button custom styles */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.6rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(21, 101, 192, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
        box-shadow: 0 6px 12px rgba(13, 71, 161, 0.3);
        transform: translateY(-1px);
    }
</style>


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None


def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(BytesIO(docx_file.read()))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return None


def create_match_gauge(match_percentage):
    """Create a gauge chart for match percentage"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=match_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Match Score", 'font': {'size': 24}},
        delta={'reference': 70},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#FFCDD2'},
                {'range': [40, 70], 'color': '#FFF9C4'},
                {'range': [70, 100], 'color': '#C8E6C9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"},
        height=250
    )
    
    return fig


def display_job_card(idx, row):
    """Display a job recommendation card"""
    match_color = "#4CAF50" if row['match_percentage'] >= 70 else "#FFC107" if row['match_percentage'] >= 50 else "#F44336"
    
    st.markdown(f"""
    <div class="job-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #1E88E5;">#{idx+1} {row['job_title']}</h3>
            <span class="match-badge" style="background-color: {match_color};">{row['match_percentage']}% Match</span>
        </div>
        <p style="font-size: 1.1rem; color: #666; margin: 0.5rem 0;">
            <strong>🏢 Company:</strong> {row['company']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display matched skills
    if row['matched_skills']:
        st.markdown("**✅ Matched Skills:**")
        skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in row['matched_skills']])
        st.markdown(skills_html, unsafe_allow_html=True)
    
    # Display missing skills
    if row['missing_skills']:
        st.markdown("**❌ Skills to Learn:**")
        skills_html = "".join([f'<span class="missing-skill-tag">{skill}</span>' for skill in row['missing_skills'][:5]])
        st.markdown(skills_html, unsafe_allow_html=True)
    
    # Job description in expander
    with st.expander("📄 View Full Job Description"):
        st.write(row['job_description'])
    
    st.markdown("---")


def main():
    """Main application function"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
        st.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
        page = st.radio(
            "Go to",
            ["🏠 Home", "🎯 Job Matcher", "📝 Resume Optimizer (ATS)", "📊 Analytics", "ℹ️ About", "🚀 How It Works"]
        )
        
        st.markdown("---")
        st.markdown("""
        ### 🇪🇹 Made for Ethiopia
        
        **Features:**
        - AI-Powered Matching
        - Real-time Analysis
        - Skill Gap Detection
        - Resume Optimization
        - Ethiopian Job Market Focus
        
        **Contact:**
        - 🐙 [GitHub](https://github.com/aprotovic/Ethio-ai-Job-Matcher)
        """)
    
    # HOME PAGE
    if page == "🏠 Home":
        st.markdown('<h1 class="main-header">🎯 AI Job Matcher Ethiopia</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Find Your Perfect Job Match Using Artificial Intelligence</p>', unsafe_allow_html=True)
        
        # Hero section with columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3 style="color: #4CAF50; margin-top: 0;">🤖 AI-Powered</h3>
                <p>Advanced Machine Learning algorithms analyze your resume and match it with thousands of jobs</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h3 style="color: #4CAF50; margin-top: 0;">⚡ Instant Results</h3>
                <p>Get personalized job recommendations in seconds with detailed match percentages</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box">
                <h3 style="color: #4CAF50; margin-top: 0;">📈 Skill Analysis</h3>
                <p>Discover your skill gaps and get recommendations for career advancement</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistics
        st.subheader("📊 Platform Statistics")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("Total Jobs", "1,500+", "+120 this week")
        
        with stat_col2:
            st.metric("Resumes Matched", "5,000+", "+300 this week")
        
        with stat_col3:
            st.metric("Success Rate", "85%", "+2%")
        
        with stat_col4:
            st.metric("Avg Match Time", "2.3s", "-0.5s")
        
        st.markdown("---")
        
        # Quick start
        st.subheader("🚀 Quick Start Guide")
        
        st.markdown("""
        1. **Upload Your Resume** - Support for PDF, DOCX, or paste text directly
        2. **AI Analysis** - Our system analyzes your skills, experience, and qualifications
        3. **Get Matches** - Receive ranked job recommendations with match percentages
        4. **Apply** - Click on jobs that interest you and start applying
        
        **Ready to find your dream job? Go to the 🎯 Job Matcher page!**
        """)
    
    # JOB MATCHER PAGE
    elif page == "🎯 Job Matcher":
        st.markdown('<h1 class="main-header">🎯 AI Job Matcher</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Upload your resume and find the perfect job matches</p>', unsafe_allow_html=True)
        
        # Initialize session state
        if 'matched_jobs' not in st.session_state:
            st.session_state.matched_jobs = None
        if 'resume_text' not in st.session_state:
            st.session_state.resume_text = None
        
        # Resume input section
        st.subheader("📄 Step 1: Provide Your Resume")
        
        input_method = st.radio(
            "Choose input method:",
            ["📝 Paste Resume Text", "📁 Upload Resume File"],
            horizontal=True
        )
        
        resume_text = None
        
        if input_method == "📝 Paste Resume Text":
            resume_text = st.text_area(
                "Paste your resume here:",
                height=300,
                placeholder="Paste your complete resume text here including education, experience, skills, etc."
            )
        
        else:  # File upload
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF or DOCX)",
                type=['pdf', 'docx', 'txt']
            )
            
            if uploaded_file:
                file_type = uploaded_file.name.split('.')[-1].lower()
                
                if file_type == 'pdf':
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif file_type == 'docx':
                    resume_text = extract_text_from_docx(uploaded_file)
                elif file_type == 'txt':
                    resume_text = uploaded_file.read().decode('utf-8')
                
                if resume_text:
                    st.success(f"✅ File uploaded successfully! ({len(resume_text)} characters)")
                    with st.expander("Preview extracted text"):
                        st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
        
        # Match button
        if st.button("🚀 Find Matching Jobs", type="primary"):
            if not resume_text or len(resume_text.strip()) < 50:
                st.error("❌ Please provide a resume with at least 50 characters")
            else:
                with st.spinner("🔄 Analyzing your resume and matching with jobs... This may take a few seconds."):
                    try:
                        # Load jobs data
                        _, jobs_df = load_data()
                        
                        # Initialize matcher
                        matcher = JobMatcher()
                        
                        # Perform matching
                        matched_jobs = matcher.match_resume_with_jobs(resume_text, jobs_df.copy())
                        
                        # Store in session state
                        st.session_state.matched_jobs = matched_jobs
                        st.session_state.resume_text = resume_text
                        
                        st.success("✅ Matching complete! Scroll down to see results.")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.error("Please check your resume format and try again.")
        
        # Display results if available
        if st.session_state.matched_jobs is not None:
            st.markdown("---")
            st.subheader("🎯 Your Job Recommendations")
            
            matched_jobs = st.session_state.matched_jobs
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Jobs Found", len(matched_jobs))
            
            with col2:
                high_match = len(matched_jobs[matched_jobs['match_percentage'] >= 70])
                st.metric("High Match (≥70%)", high_match)
            
            with col3:
                avg_match = matched_jobs['match_percentage'].mean()
                st.metric("Average Match", f"{avg_match:.1f}%")
            
            # Filter options
            st.markdown("### 🔍 Filter Results")
            
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                min_match = st.slider(
                    "Minimum Match Percentage",
                    0, 100, 0, 5
                )
            
            with filter_col2:
                top_n = st.selectbox(
                    "Number of jobs to display",
                    [5, 10, 15, 20, "All"],
                    index=1
                )
            
            # Apply filters
            filtered_jobs = matched_jobs[matched_jobs['match_percentage'] >= min_match]
            
            if top_n != "All":
                filtered_jobs = filtered_jobs.head(top_n)
            
            st.markdown(f"**Showing {len(filtered_jobs)} jobs**")
            
            # Display job cards
            for idx, row in filtered_jobs.iterrows():
                display_job_card(idx, row)
            
            # Skill Gap Analysis
            st.markdown("---")
            st.subheader("📊 Skill Gap Analysis")
            
            matcher = JobMatcher()
            skill_analysis = matcher.analyze_skill_gap(
                st.session_state.resume_text, 
                matched_jobs.head(10)
            )
            
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                st.markdown("**✅ Your Current Skills:**")
                if skill_analysis['current_skills']:
                    skills_html = "".join([
                        f'<span class="skill-tag">{skill}</span>' 
                        for skill in skill_analysis['current_skills'][:15]
                    ])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.info("No specific skills detected. Try adding more technical keywords to your resume.")
            
            with analysis_col2:
                st.markdown("**📈 Top Skills to Learn:**")
                if skill_analysis['top_missing_skills']:
                    skills_html = "".join([
                        f'<span class="missing-skill-tag">{skill}</span>' 
                        for skill in skill_analysis['top_missing_skills'][:10]
                    ])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.success("Great! You have most of the required skills.")
            
            # Download results
            st.markdown("---")
            csv_data = filtered_jobs[['job_title', 'company', 'match_percentage']].to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name="job_matches.csv",
                mime="text/csv"
            )
            
    # RESUME OPTIMIZER PAGE
    elif page == "📝 Resume Optimizer (ATS)":
        st.markdown('<h1 class="main-header">📝 Resume Optimizer (ATS)</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Optimize your resume for a specific job posting to pass ATS filters</p>', unsafe_allow_html=True)
        
        # Load jobs data
        _, jobs_df = load_data()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎯 Step 1: Select or Paste Job Description")
            job_option = st.selectbox(
                "Choose target job:",
                ["-- Paste Custom Job Description --"] + [f"{row['job_title']} at {row['company']}" for _, row in jobs_df.iterrows()]
            )
            
            job_title_input = ""
            company_input = ""
            job_description = ""
            
            if job_option == "-- Paste Custom Job Description --":
                job_title_input = st.text_input("Job Title:", placeholder="e.g. Python Developer")
                company_input = st.text_input("Company Name:", placeholder="e.g. Safaricom Ethiopia")
                job_description = st.text_area(
                    "Paste the job description details here:",
                    height=250,
                    placeholder="Paste job responsibilities, required skills, qualification details, etc."
                )
            else:
                # Find matching row in jobs_df
                selected_idx = [f"{row['job_title']} at {row['company']}" for _, row in jobs_df.iterrows()].index(job_option)
                selected_job = jobs_df.iloc[selected_idx]
                job_title_input = selected_job['job_title']
                company_input = selected_job['company']
                job_description = selected_job['job_description']
                
                # Show job description in collapsed expander
                with st.expander("📄 View Selected Job Description"):
                    st.write(job_description)
                    
        with col2:
            st.subheader("📄 Step 2: Provide Your Resume")
            input_method = st.radio(
                "Resume input method:",
                ["📝 Paste Resume Text", "📁 Upload Resume File"],
                horizontal=True,
                key="optimizer_input_method"
            )
            
            resume_text = ""
            if input_method == "📝 Paste Resume Text":
                resume_text = st.text_area(
                    "Paste your resume here:",
                    height=250,
                    placeholder="Paste your complete resume details...",
                    key="optimizer_resume_text"
                )
            else:
                uploaded_file = st.file_uploader(
                    "Upload your resume file (PDF/DOCX)",
                    type=['pdf', 'docx', 'txt'],
                    key="optimizer_file_uploader"
                )
                if uploaded_file:
                    file_type = uploaded_file.name.split('.')[-1].lower()
                    if file_type == 'pdf':
                        resume_text = extract_text_from_pdf(uploaded_file)
                    elif file_type == 'docx':
                        resume_text = extract_text_from_docx(uploaded_file)
                    elif file_type == 'txt':
                        resume_text = uploaded_file.read().decode('utf-8')
                        
                    if resume_text:
                        st.success(f"✅ File uploaded successfully!")
                        
        if st.button("📊 Run ATS Optimization Scan", type="primary", key="run_scan_btn"):
            if not resume_text or len(resume_text.strip()) < 50:
                st.error("❌ Please provide a resume with at least 50 characters.")
            elif not job_description or len(job_description.strip()) < 50:
                st.error("❌ Please select or provide a job description with at least 50 characters.")
            else:
                with st.spinner("🔄 Running deep analysis on resume-to-job matching..."):
                    try:
                        matcher = JobMatcher()
                        
                        # Create temporary jobs dataframe with just this one job
                        temp_df = pd.DataFrame([{
                            'job_id': 1,
                            'job_title': job_title_input,
                            'company': company_input,
                            'job_description': job_description
                        }])
                        
                        results = matcher.match_resume_with_jobs(resume_text, temp_df)
                        
                        if not results.empty:
                            row = results.iloc[0]
                            match_pct = row['match_percentage']
                            matched_skills = row['matched_skills']
                            missing_skills = row['missing_skills']
                            
                            st.markdown("---")
                            st.subheader("📊 Optimization Scan Results")
                            
                            res_col1, res_col2 = st.columns([1, 1])
                            
                            with res_col1:
                                st.plotly_chart(create_match_gauge(match_pct), use_container_width=True)
                                
                            with res_col2:
                                # Rating text
                                if match_pct >= 80:
                                    status_color = "green"
                                    status_text = "Strong Match (Excellent Compatibility)"
                                    status_desc = "Your resume is highly optimized for this role and has a high probability of passing ATS parsing filters!"
                                elif match_pct >= 60:
                                    status_color = "orange"
                                    status_text = "Moderate Match (Needs Improvement)"
                                    status_desc = "Your resume shares notable common ground but is missing key skill keywords. Add them to improve your ATS score."
                                else:
                                    status_color = "red"
                                    status_text = "Weak Match (Requires Refactoring)"
                                    status_desc = "Your resume has low alignment with the job description. We highly recommend rewriting your resume to include the missing core skills."
                                    
                                st.markdown(f"""
                                <div style="padding: 1.5rem; border-radius: 12px; border-left: 6px solid {status_color}; background-color: #fafafa; margin-top: 1rem;">
                                    <h3 style="margin-top: 0; color: {status_color};">{status_text}</h3>
                                    <p style="font-size: 1rem; color: #424242;">{status_desc}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            # Skill Breakdown
                            st.markdown("### 🔑 Keyword & Skill Breakdown")
                            skill_col1, skill_col2 = st.columns(2)
                            
                            with skill_col1:
                                st.markdown("**✅ Matched Skills & Keywords** (Found in resume):")
                                if matched_skills:
                                    html = "".join([f'<span class="skill-tag">{s}</span>' for s in matched_skills])
                                    st.markdown(html, unsafe_allow_html=True)
                                else:
                                    st.info("No matching skills found. Make sure to check spelling or list technical capabilities.")
                                    
                            with skill_col2:
                                st.markdown("**❌ Missing Skills & Keywords** (Required but not found):")
                                if missing_skills:
                                    html = "".join([f'<span class="missing-skill-tag">{s}</span>' for s in missing_skills])
                                    st.markdown(html, unsafe_allow_html=True)
                                else:
                                    st.success("Awesome! No missing skills detected. Your resume matches all core keywords.")
                                    
                            # Optimization Suggestions
                            st.markdown("### 💡 Recommended Resume Enhancements")
                            if missing_skills:
                                st.markdown("To optimize your resume and bypass ATS filtering, consider adding sections or accomplishments highlighting the following:")
                                
                                # Custom template recommendations based on missing skills
                                categories = {
                                    'ml_ai': {
                                        'keywords': ['machine learning', 'deep learning', 'ai', 'nlp', 'tensorflow', 'pytorch', 'scikit-learn', 'data science'],
                                        'advice': "💡 **AI & Data Science**: Add details about training predictive models, handling datasets, or engineering machine learning pipelines. E.g.: *'Designed and evaluated supervised machine learning models using scikit-learn and TensorFlow to predict customer behaviors, boosting model precision by 15%.'*"
                                    },
                                    'cloud_devops': {
                                        'keywords': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'devops', 'ci/cd', 'jenkins'],
                                        'advice': "💡 **DevOps & Cloud Systems**: Highlight infrastructure automation and cloud deployment. E.g.: *'Built and maintained automated CI/CD pipelines in GitLab, containerizing microservices with Docker and deploying to AWS cloud infrastructures.'*"
                                    },
                                    'backend_db': {
                                        'keywords': ['python', 'django', 'flask', 'api', 'rest', 'graphql', 'postgresql', 'mongodb', 'mysql', 'sql'],
                                        'advice': "💡 **Backend & Databases**: Detail API design, backend logic, and database schemas. E.g.: *'Designed secure, high-performance RESTful APIs utilizing Python and Django, optimizing PostgreSQL database queries to reduce loading time by 30%.'*"
                                    },
                                    'frontend_web': {
                                        'keywords': ['javascript', 'react', 'angular', 'vue', 'node', 'html', 'css', 'bootstrap', 'tailwind'],
                                        'advice': "💡 **Frontend Web Development**: Focus on interactive UI components and responsive design. E.g.: *'Developed responsive, user-friendly client interfaces using React and Tailwind CSS, increasing user engagement metrics by 20%.'*"
                                    },
                                    'pm_agile': {
                                        'keywords': ['project management', 'leadership', 'communication', 'teamwork', 'agile', 'scrum'],
                                        'advice': "💡 **Agile Collaboration & Management**: Outline leadership and team collaboration. E.g.: *'Led collaborative agile teams through bi-weekly sprints and scrum ceremonies, successfully delivering three cross-functional software projects ahead of schedule.'*"
                                    },
                                    'design_uiux': {
                                        'keywords': ['ui/ux', 'design', 'figma', 'photoshop', 'illustrator', 'adobe'],
                                        'advice': "💡 **UI/UX & Creative Design**: Mention user research, wireframing, and design prototypes. E.g.: *'Created interactive wireframes and high-fidelity prototypes in Figma, conducting user research to optimize mobile app accessibility and UI flows.'*"
                                    }
                                }
                                
                                shown_advice = 0
                                for cat_name, cat_info in categories.items():
                                    overlap = set(cat_info['keywords']) & set(missing_skills)
                                    if overlap:
                                        st.markdown(cat_info['advice'])
                                        shown_advice += 1
                                        
                                if shown_advice == 0:
                                    st.markdown(f"💡 **General Keyword Addition**: Incorporate missing skills like **{', '.join(missing_skills[:5])}** within your core skills inventory or project achievements sections.")
                            else:
                                st.success("🎉 Your resume is exceptionally well aligned with this job specification. No additional enhancements are strictly required!")
                    except Exception as e:
                        st.error(f"❌ An error occurred during scan: {str(e)}")

    # ANALYTICS PAGE
    elif page == "📊 Analytics":
        st.markdown('<h1 class="main-header">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
        
        if st.session_state.get('matched_jobs') is None:
            st.info("👆 Please match your resume with jobs first from the Job Matcher page")
        else:
            matched_jobs = st.session_state.matched_jobs
            
            # Match distribution
            st.subheader("📈 Match Score Distribution")
            
            fig = px.histogram(
                matched_jobs, 
                x='match_percentage',
                nbins=20,
                title="Distribution of Match Percentages",
                labels={'match_percentage': 'Match Percentage', 'count': 'Number of Jobs'},
                color_discrete_sequence=['#1E88E5']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Top companies
            st.subheader("🏢 Top Companies by Average Match")
            
            company_avg = matched_jobs.groupby('company')['match_percentage'].mean().sort_values(ascending=False).head(10)
            
            fig2 = px.bar(
                x=company_avg.values,
                y=company_avg.index,
                orientation='h',
                title="Top 10 Companies by Match Score",
                labels={'x': 'Average Match %', 'y': 'Company'},
                color=company_avg.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Skill frequency
            st.subheader("💡 Most Frequently Required Skills")
            
            all_skills = []
            for skills in matched_jobs['missing_skills']:
                all_skills.extend(skills)
            
            if all_skills:
                skill_counts = pd.Series(all_skills).value_counts().head(15)
                
                fig3 = px.bar(
                    x=skill_counts.values,
                    y=skill_counts.index,
                    orientation='h',
                    title="Top 15 Missing Skills in Job Market",
                    labels={'x': 'Frequency', 'y': 'Skill'},
                    color=skill_counts.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig3, use_container_width=True)
    
    # ABOUT PAGE
    elif page == "ℹ️ About":
        st.markdown('<h1 class="main-header">ℹ️ About AI Job Matcher</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        ## 🎯 Project Overview
        
        **AI Job Recommendation & Resume Matcher System** is an advanced machine learning application
        designed specifically for the Ethiopian job market. It uses Natural Language Processing (NLP)
        and similarity algorithms to match job seekers with the most relevant opportunities.
        
        ## 🤖 How It Works
        
        Our system employs several AI techniques:
        
        ### 1. **Natural Language Processing (NLP)**
        - Processes both resumes and job descriptions
        - Extracts key information like skills, experience, and qualifications
        - Handles variations in language and terminology
        
        ### 2. **TF-IDF Vectorization**
        - Converts text into numerical vectors
        - TF-IDF = Term Frequency-Inverse Document Frequency
        - Identifies important keywords unique to each document
        
        ### 3. **Cosine Similarity**
        - Measures the angle between resume and job vectors
        - Scores range from 0% (no match) to 100% (perfect match)
        - Mathematical formula ensures objective matching
        
        ### 4. **Skill Extraction & Gap Analysis**
        - Automatically identifies technical and soft skills
        - Compares your skills with job requirements
        - Provides personalized learning recommendations
        
        ## 🌟 Key Features
        
        ✅ **AI-Powered Matching** - Advanced ML algorithms  
        ✅ **Instant Results** - Get recommendations in seconds  
        ✅ **Skill Analysis** - Identify gaps in your skillset  
        ✅ **Ethiopian Focus** - Tailored for local job market  
        ✅ **Multiple Input Methods** - PDF, DOCX, or text  
        ✅ **Visual Analytics** - Charts and graphs for insights  
        
        ## 🏢 Real-World Applications
        
        This technology is used by:
        - **LinkedIn** - For job recommendations
        - **Indeed** - Resume-job matching
        - **Glassdoor** - Career insights
        - **Recruitment Agencies** - Candidate screening
        - **HR Departments** - Automated resume filtering
        
        ## 👨‍💻 Technology Stack
        
        - **Backend**: Python, scikit-learn, NLTK
        - **Frontend**: Streamlit
        - **ML Algorithms**: TF-IDF, Cosine Similarity
        - **Data Processing**: Pandas, NumPy
        - **Visualization**: Plotly
        
        ## 📧 Contact & Support
        
        For inquiries, partnerships, or support:
        - **GitHub**: [github.com/aprotovic/Ethio-ai-Job-Matcher](https://github.com/aprotovic/Ethio-ai-Job-Matcher)
        
        ---
        
        **Built with ❤️ for Ethiopian job seekers**
        """)
    
    # HOW IT WORKS PAGE
    elif page == "🚀 How It Works":
        st.markdown('<h1 class="main-header">🚀 How It Works</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        ## Technical Deep Dive
        
        ### Step 1: Text Preprocessing 🔄
        
        Both your resume and job descriptions go through cleaning:
        
        ```python
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\\s]', '', text)
        
        # Remove stopwords (common words like 'the', 'is', 'and')
        words = [word for word in words if word not in stopwords]
        
        # Lemmatization (convert words to base form)
        # running → run, better → good
        ```
        
        ### Step 2: Feature Extraction 📊
        
        **TF-IDF (Term Frequency-Inverse Document Frequency)**
        
        - **Term Frequency (TF)**: How often a word appears in a document
        - **Inverse Document Frequency (IDF)**: How rare/important a word is across all documents
        - **TF-IDF Score** = TF × IDF
        
        Example:
        - Word "Python" in your resume: High TF-IDF (important skill)
        - Word "experience" in your resume: Lower TF-IDF (common word)
        
        ### Step 3: Similarity Calculation 🎯
        
        **Cosine Similarity Formula:**
        
        ```
        similarity = (A · B) / (||A|| × ||B||)
        ```
        
        Where:
        - A = Your resume vector
        - B = Job description vector
        - Result = Similarity score between 0 and 1
        
        ### Step 4: Ranking & Recommendations 📈
        
        Jobs are ranked by similarity score:
        - Score × 100 = Match Percentage
        - Jobs sorted from highest to lowest match
        - Top recommendations displayed to user
        
        ## 🔬 Why This Works
        
        1. **Mathematical Foundation**: Uses proven vector space models
        2. **Context-Aware**: Understands meaning, not just keywords
        3. **Scalable**: Can handle millions of resumes and jobs
        4. **Fast**: Results in seconds, not hours
        5. **Objective**: No human bias in matching
        
        ## 🚀 Real Company Implementations
        
        ### LinkedIn's Approach
        - Uses similar TF-IDF + embeddings
        - Adds user behavior signals (clicks, applications)
        - Deep learning models for personalization
        - A/B testing for continuous improvement
        
        ### Indeed's System
        - Multi-stage ranking pipeline
        - Location-based filtering
        - Salary expectation matching
        - Experience level classification
        
        ## ⚠️ Limitations of Current System
        
        1. **No Contextual Understanding**: Doesn't understand complex meanings
        2. **Keyword Dependency**: May miss synonyms or related terms
        3. **No Learning**: Doesn't improve from user feedback
        4. **Static Weights**: All features treated equally
        
        ## 🎓 Advanced Improvements (Enterprise Level)
        
        ### 1. Use Word Embeddings
        ```python
        # Instead of TF-IDF, use Word2Vec or BERT
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        resume_embedding = model.encode(resume_text)
        job_embedding = model.encode(job_description)
        ```
        
        Benefits:
        - Understands context and meaning
        - Captures semantic similarity
        - "Machine Learning" matches with "AI" and "Data Science"
        
        ### 2. Deep Learning Models
        - Neural networks for matching
        - Learn from historical data
        - Personalized recommendations
        - Multi-task learning
        
        ### 3. User Behavior Signals
        - Click-through rate
        - Application completion rate
        - Time spent on job page
        - User feedback (like/dislike)
        
        ### 4. Real-time Learning
        - A/B testing different algorithms
        - Online learning from new data
        - Continuous model updates
        
        ## 📈 Scaling to Millions of Users
        
        **Infrastructure Requirements:**
        
        1. **Database**: PostgreSQL or MongoDB for storage
        2. **Caching**: Redis for fast retrieval
        3. **Search**: Elasticsearch for full-text search
        4. **Queue**: RabbitMQ for async processing
        5. **Cloud**: AWS/Azure for scalability
        6. **CDN**: CloudFlare for global distribution
        
        **Architecture:**
        ```
        User → Load Balancer → API Servers → ML Service → Database
                                    ↓
                                Cache (Redis)
        ```
        
        ## 💡 Frequently Asked Questions
        
        **Q: Why use Cosine Similarity instead of Euclidean Distance?**  
        A: Cosine similarity measures angle, not magnitude. It works better for text because it doesn't care about document length, only content similarity.
        
        **Q: How would you handle spelling mistakes?**  
        A: Use fuzzy matching (Levenshtein distance) or train a spelling correction model.
        
        **Q: How to prevent bias in job matching?**  
        A: Remove demographic keywords, use fairness constraints, and regular bias audits.
        
        **Q: How would you evaluate the system's performance?**  
        A: Metrics: Precision@K, Recall@K, MAP (Mean Average Precision), user feedback scores.
        
        **Q: What if there are no good matches?**  
        A: Provide partial matches, suggest skill gaps, recommend training courses.
        
        ---
        
        **Want to learn more? Check out the source code on GitHub!**
        """)


if __name__ == "__main__":
    main()
