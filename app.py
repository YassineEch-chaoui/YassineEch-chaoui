import streamlit as st
import requests
import time
import json
from datetime import datetime
import base64
import io

# Basic configuration
st.set_page_config(
    page_title="Yassine Ech-chaoui - Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hardcoded configuration values
GITHUB_API_URL = "https://api.github.com"
GITHUB_USERNAME = "YassineEch-chaoui"
PRIMARY_COLOR = "#FF6B6B"
SECONDARY_COLOR = "#4ECDC4"
BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#333333"

# Basic CSS styling
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #4ECDC4;
        border-bottom: 2px solid #4ECDC4;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    .tech-badge {
        display: inline-block;
        background-color: #FF6B6B;
        color: white;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    .project-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .contact-info {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to get GitHub data
def get_github_repos():
    try:
        response = requests.get(f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/repos")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch GitHub repositories")
            return []
    except Exception as e:
        st.error(f"Error fetching GitHub data: {str(e)}")
        return []

# Function to get GitHub user info
def get_github_user():
    try:
        response = requests.get(f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch GitHub user info")
            return {}
    except Exception as e:
        st.error(f"Error fetching GitHub user data: {str(e)}")
        return {}

# Main application
def main():
    load_css()
    
    # Header
    st.markdown('<h1 class="main-header">💻 Yassine Ech-chaoui</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Software Developer & Tech Enthusiast</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose a section:", [
        "About Me", 
        "Skills & Technologies", 
        "Projects", 
        "GitHub Stats", 
        "Contact"
    ])
    
    if page == "About Me":
        show_about()
    elif page == "Skills & Technologies":
        show_skills()
    elif page == "Projects":
        show_projects()
    elif page == "GitHub Stats":
        show_github_stats()
    elif page == "Contact":
        show_contact()

def show_about():
    st.markdown('<h2 class="section-header">👨‍💻 About Me</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        ### Hello there! 👋
        
        I'm Yassine, a passionate software developer who turns ideas into apps and caffeine into code ☕💡
        
        **What drives me:**
        - 🔥 Powered by memes and deadlines
        - 🧠 Collecting knowledge like it's Pokémon
        - 💡 Turning curiosity into creation
        - 💪 Gym rat with a GitHub account
        - 🗡️ Coding like Thorfinn fights: with patience, purpose, and rage
        
        I'm constantly learning and exploring new technologies, building projects that solve real-world problems,
        and contributing to the developer community.
        """)
    
    with col2:
        st.image("https://media.giphy.com/media/SWoSkN6DxTszqIKEqv/giphy.gif", width=300)

def show_skills():
    st.markdown('<h2 class="section-header">🛠️ Skills & Technologies</h2>', unsafe_allow_html=True)
    
    skills = {
        "Programming Languages": [
            "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "Kotlin", "PowerShell", "Bash"
        ],
        "Web Technologies": [
            "HTML5", "CSS3", "React", "Flask", "Django", "Laravel"
        ],
        "Databases": [
            "MySQL", "MongoDB", "Microsoft SQL Server"
        ],
        "Cloud & DevOps": [
            "Azure", "Oracle", "Docker", "Git", "Apache"
        ],
        "Tools & Others": [
            "LaTeX", "Postman", "Anaconda", ".NET"
        ]
    }
    
    for category, tech_list in skills.items():
        st.markdown(f"### {category}")
        tech_badges = "".join([f'<span class="tech-badge">{tech}</span>' for tech in tech_list])
        st.markdown(tech_badges, unsafe_allow_html=True)
        st.write("")

def show_projects():
    st.markdown('<h2 class="section-header">🚀 Projects</h2>', unsafe_allow_html=True)
    
    # Show loading spinner
    with st.spinner("Loading projects from GitHub..."):
        repos = get_github_repos()
    
    if repos:
        # Filter and sort repositories
        filtered_repos = [repo for repo in repos if not repo['fork'] and repo['description']]
        filtered_repos.sort(key=lambda x: x['updated_at'], reverse=True)
        
        for repo in filtered_repos[:6]:  # Show top 6 projects
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <h3>🔗 {repo['name']}</h3>
                    <p>{repo['description']}</p>
                    <p><strong>Language:</strong> {repo['language'] or 'N/A'}</p>
                    <p><strong>⭐ Stars:</strong> {repo['stargazers_count']} | <strong>🍴 Forks:</strong> {repo['forks_count']}</p>
                    <a href="{repo['html_url']}" target="_blank">View on GitHub →</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No projects found or unable to load GitHub repositories.")

def show_github_stats():
    st.markdown('<h2 class="section-header">📊 GitHub Statistics</h2>', unsafe_allow_html=True)
    
    with st.spinner("Loading GitHub stats..."):
        user_data = get_github_user()
    
    if user_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Public Repos", user_data.get('public_repos', 0))
        
        with col2:
            st.metric("Followers", user_data.get('followers', 0))
        
        with col3:
            st.metric("Following", user_data.get('following', 0))
        
        with col4:
            st.metric("Public Gists", user_data.get('public_gists', 0))
        
        st.markdown("---")
        
        # Show GitHub profile link
        if user_data.get('html_url'):
            st.markdown(f"🔗 [View Full GitHub Profile]({user_data['html_url']})")
        
        # Show contribution stats
        st.markdown("### 📈 Contribution Stats")
        st.image(f"https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&theme=bear&hide_border=false&include_all_commits=false&count_private=false")
        
        st.markdown("### 📊 Most Used Languages")
        st.image(f"https://github-readme-stats.vercel.app/api/top-langs/?username={GITHUB_USERNAME}&theme=bear&hide_border=false&include_all_commits=false&count_private=false&layout=compact")

def show_contact():
    st.markdown('<h2 class="section-header">📬 Get In Touch</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="contact-info">
            <h3>📧 Contact Information</h3>
            <p>I'm always open to discussing new opportunities, collaborations, or just having a chat about technology!</p>
            
            <p><strong>🐙 GitHub:</strong> <a href="https://github.com/YassineEch-chaoui" target="_blank">YassineEch-chaoui</a></p>
            <p><strong>💼 Professional Networks:</strong> Feel free to connect with me on professional platforms</p>
            <p><strong>📩 Email:</strong> Available upon request</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💌 Send me a message")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            subject = st.text_input("Subject")
            message = st.text_area("Message", height=100)
            
            submitted = st.form_submit_button("Send Message")
            
            if submitted:
                if name and email and message:
                    # Simulate sending message
                    with st.spinner("Sending message..."):
                        time.sleep(2)
                    st.success("Thank you for your message! I'll get back to you soon.")
                else:
                    st.error("Please fill in all required fields.")

# Session state management
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 0

st.session_state.visit_count += 1

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>© 2024 Yassine Ech-chaoui | Visit #{st.session_state.visit_count}</p>
    <p>Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()