"""
Configuration constants for the Streamlit Portfolio Application
"""
import os
from typing import Dict, List

# Application Configuration
APP_TITLE = "Yassine Ech-chaoui - Portfolio"
APP_ICON = "💻"
APP_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Personal Information
DEVELOPER_NAME = "Yassine Ech-chaoui"
DEVELOPER_TAGLINE = "Software Developer & Tech Enthusiast"
GITHUB_USERNAME = "YassineEch-chaoui"

# API Configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_API_TIMEOUT = 10

# UI Theme Colors
THEME_COLORS = {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4", 
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# Dark Theme Colors
DARK_THEME_COLORS = {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4",
    "background": "#0E1117",
    "surface": "#262730",
    "text_primary": "#FAFAFA",
    "text_secondary": "#BFBFBF",
    "border": "#3D4043"
}

# Light Theme Colors  
LIGHT_THEME_COLORS = {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4", 
    "background": "#FFFFFF",
    "surface": "#F8F9FA",
    "text_primary": "#333333",
    "text_secondary": "#666666",
    "border": "#DEE2E6"
}

# Navigation Configuration
NAVIGATION_ITEMS = [
    "About Me",
    "Skills & Technologies", 
    "Projects",
    "GitHub Stats",
    "Contact"
]

# Skills Configuration
SKILLS_CATEGORIES = {
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

# About Me Content
ABOUT_ME_CONTENT = {
    "greeting": "Hello there! 👋",
    "intro": "I'm Yassine, a passionate software developer who turns ideas into apps and caffeine into code ☕💡",
    "traits": [
        "🔥 Powered by memes and deadlines",
        "🧠 Collecting knowledge like it's Pokémon", 
        "💡 Turning curiosity into creation",
        "💪 Gym rat with a GitHub account",
        "🗡️ Coding like Thorfinn fights: with patience, purpose, and rage"
    ],
    "description": """I'm constantly learning and exploring new technologies, building projects that solve real-world problems,
    and contributing to the developer community.""",
    "gif_url": "https://media.giphy.com/media/SWoSkN6DxTszqIKEqv/giphy.gif"
}

# Contact Information
CONTACT_INFO = {
    "github_url": f"https://github.com/{GITHUB_USERNAME}",
    "description": "I'm always open to discussing new opportunities, collaborations, or just having a chat about technology!"
}

# Repository Filtering
MAX_REPOS_DISPLAY = 6

# Environment Variables (with defaults)
API_KEYS = {
    "github_token": os.getenv("GITHUB_TOKEN", ""),
    "email_service": os.getenv("EMAIL_SERVICE_KEY", "")
}

# Cache Configuration
CACHE_TTL = 3600  # 1 hour in seconds

# Error Messages
ERROR_MESSAGES = {
    "github_api_error": "Failed to fetch GitHub data. Please try again later.",
    "network_error": "Network error occurred. Please check your connection.",
    "validation_error": "Please fill in all required fields.",
    "generic_error": "An unexpected error occurred. Please try again."
}

# Loading Messages
LOADING_MESSAGES = {
    "github_repos": "Loading projects from GitHub...",
    "github_stats": "Loading GitHub stats...",
    "sending_message": "Sending message..."
}

# Success Messages
SUCCESS_MESSAGES = {
    "message_sent": "Thank you for your message! I'll get back to you soon."
}