"""
Theme management utility for adaptive dark/light mode support
"""
import streamlit as st
from typing import Dict, Optional
from config.constants import DARK_THEME_COLORS, LIGHT_THEME_COLORS, THEME_COLORS

class ThemeManager:
    """Manages theme detection and CSS generation for dark/light modes"""
    
    def __init__(self):
        self.current_theme = self._detect_streamlit_theme()
    
    def _detect_streamlit_theme(self) -> str:
        """
        Detect current Streamlit theme
        Returns 'dark' or 'light' based on Streamlit's theme
        """
        # Check if we can detect theme from Streamlit's context
        try:
            # This is a workaround since Streamlit doesn't expose theme directly
            # We'll use CSS injection to detect the theme
            return st.session_state.get('detected_theme', 'auto')
        except:
            return 'auto'
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get colors for current theme"""
        if self.current_theme == 'dark':
            return DARK_THEME_COLORS
        elif self.current_theme == 'light':
            return LIGHT_THEME_COLORS
        else:
            return THEME_COLORS
    
    def generate_adaptive_css(self) -> str:
        """Generate CSS that adapts to both dark and light themes"""
        colors = self.get_theme_colors()
        
        return f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Reset and base styles */
        .main .block-container {{
            font-family: 'Inter', sans-serif;
            max-width: 1200px;
            padding-top: 2rem;
        }}
        
        /* Adaptive variables for both themes */
        :root {{
            --primary-color: {colors['primary']};
            --secondary-color: {colors['secondary']};
            --background-color: {colors.get('background', '#FFFFFF')};
            --surface-color: {colors.get('surface', '#F8F9FA')};
            --text-primary: {colors.get('text_primary', '#333333')};
            --text-secondary: {colors.get('text_secondary', '#666666')};
            --border-color: {colors.get('border', '#DEE2E6')};
        }}
        
        /* Dark theme overrides */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --background-color: #0E1117;
                --surface-color: #262730;
                --text-primary: #FAFAFA;
                --text-secondary: #BFBFBF;
                --border-color: #3D4043;
            }}
        }}
        
        /* Header styles */
        .main-header {{
            font-size: 3rem;
            font-weight: 700;
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .main-subtitle {{
            text-align: center;
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 3rem;
            font-weight: 400;
        }}
        
        /* Section headers */
        .section-header {{
            font-size: 2rem;
            font-weight: 600;
            color: var(--text-primary);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 0.5rem;
            margin: 2rem 0 1rem 0;
            position: relative;
        }}
        
        .section-header::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 50px;
            height: 2px;
            background: var(--primary-color);
        }}
        
        /* Tech badges */
        .tech-badge {{
            display: inline-block;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 0.4rem 1rem;
            margin: 0.3rem 0.2rem;
            border-radius: 25px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);
        }}
        
        .tech-badge:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(255, 107, 107, 0.3);
        }}
        
        /* Project cards */
        .project-card {{
            border: 1px solid var(--border-color);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            background: var(--surface-color);
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        .project-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            border-color: var(--primary-color);
        }}
        
        .project-card h3 {{
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-weight: 600;
        }}
        
        .project-card p {{
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .project-card a {{
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        
        .project-card a:hover {{
            color: var(--primary-color);
        }}
        
        /* Contact info */
        .contact-info {{
            background: var(--surface-color);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        .contact-info h3 {{
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-weight: 600;
        }}
        
        .contact-info p {{
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .contact-info a {{
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: 500;
        }}
        
        /* Metric cards */
        .metric-card {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        }}
        
        /* Sidebar enhancements */
        .css-1d391kg {{
            background: var(--surface-color);
        }}
        
        /* Button styles */
        .stButton > button {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.6rem 2rem;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
        }}
        
        /* Form inputs */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            border: 2px solid var(--border-color);
            border-radius: 10px;
            background: var(--surface-color);
            color: var(--text-primary);
            transition: border-color 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
        }}
        
        /* Loading spinner */
        .stSpinner {{
            color: var(--primary-color);
        }}
        
        /* Success/Error messages */
        .stSuccess {{
            background: rgba(40, 167, 69, 0.1);
            border: 1px solid rgba(40, 167, 69, 0.3);
            border-radius: 10px;
        }}
        
        .stError {{
            background: rgba(220, 53, 69, 0.1);
            border: 1px solid rgba(220, 53, 69, 0.3);
            border-radius: 10px;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            color: var(--text-secondary);
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .main-header {{
                font-size: 2rem;
            }}
            
            .section-header {{
                font-size: 1.5rem;
            }}
            
            .project-card,
            .contact-info {{
                padding: 1rem;
            }}
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .fade-in-up {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        /* Theme toggle button */
        .theme-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        .theme-toggle:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }}
        </style>
        """
    
    def inject_theme_detector(self) -> str:
        """Inject JavaScript to detect system theme preference"""
        return """
        <script>
        // Detect system theme preference
        function detectTheme() {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return 'dark';
            } else {
                return 'light';
            }
        }
        
        // Store theme preference
        const theme = detectTheme();
        window.parent.document.body.setAttribute('data-theme', theme);
        
        // Listen for theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                const newTheme = e.matches ? 'dark' : 'light';
                window.parent.document.body.setAttribute('data-theme', newTheme);
            });
        }
        </script>
        """
    
    def get_loading_css(self) -> str:
        """Get CSS for loading animations"""
        return """
        <style>
        .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid var(--border-color);
            border-top: 4px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """