"""
Application settings and configuration management
"""
import streamlit as st
from typing import Dict, Any
from config.constants import *

class AppSettings:
    """Manages application settings and configuration"""
    
    def __init__(self):
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'visit_count' not in st.session_state:
            st.session_state.visit_count = 0
            
        if 'theme_preference' not in st.session_state:
            st.session_state.theme_preference = self.detect_theme()
            
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {
                'animations_enabled': True,
                'auto_refresh': False,
                'compact_mode': False
            }
    
    def detect_theme(self) -> str:
        """Detect user's preferred theme"""
        # Try to detect theme from browser/system
        # For now, default to 'auto' which will adapt to Streamlit's theme
        return 'auto'
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get appropriate theme colors based on current theme"""
        if st.session_state.theme_preference == 'dark':
            return DARK_THEME_COLORS
        elif st.session_state.theme_preference == 'light':
            return LIGHT_THEME_COLORS
        else:
            # Auto-detect or use default
            return THEME_COLORS
    
    def update_visit_count(self):
        """Update visit counter"""
        st.session_state.visit_count += 1
    
    def get_page_config(self) -> Dict[str, Any]:
        """Get Streamlit page configuration"""
        return {
            "page_title": APP_TITLE,
            "page_icon": APP_ICON,
            "layout": APP_LAYOUT,
            "initial_sidebar_state": SIDEBAR_STATE
        }
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference value"""
        return st.session_state.user_preferences.get(key, default)
    
    def set_user_preference(self, key: str, value: Any):
        """Set user preference value"""
        st.session_state.user_preferences[key] = value
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current = st.session_state.theme_preference
        if current == 'light':
            st.session_state.theme_preference = 'dark'
        elif current == 'dark':
            st.session_state.theme_preference = 'light'
        else:
            st.session_state.theme_preference = 'light'
    
    @staticmethod
    def is_development_mode() -> bool:
        """Check if running in development mode"""
        return os.getenv('STREAMLIT_ENV', 'production') == 'development'