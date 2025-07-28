"""
Refactored Streamlit Portfolio Application
Modern, modular architecture with comprehensive features
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Import configuration and components
from config.settings import AppSettings
from config.constants import *
from components.header import HeaderComponent
from components.sidebar import SidebarComponent
from components.sections.about import AboutSection
from components.sections.skills import SkillsSection
from components.sections.projects import ProjectsSection
from components.sections.github_stats import GitHubStatsSection
from components.sections.contact import ContactSection
from components.base import NotificationManager
from utils.theme_manager import ThemeManager
from utils.cache_manager import performance_monitor

class PortfolioApp:
    """Main Portfolio Application Class"""
    
    def __init__(self):
        self.load_environment()
        self.settings = AppSettings()
        self.theme_manager = ThemeManager()
        self.notification_manager = NotificationManager()
        self.setup_page_config()
        self.initialize_components()
    
    def load_environment(self):
        """Load environment variables"""
        load_dotenv()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        page_config = self.settings.get_page_config()
        st.set_page_config(**page_config)
    
    def initialize_components(self):
        """Initialize all application components"""
        self.header = HeaderComponent(self.theme_manager)
        self.sidebar = SidebarComponent(self.theme_manager)
        self.about_section = AboutSection(self.theme_manager)
        self.skills_section = SkillsSection(self.theme_manager)
        self.projects_section = ProjectsSection(self.theme_manager)
        self.github_stats_section = GitHubStatsSection(self.theme_manager)
        self.contact_section = ContactSection(self.theme_manager)
    
    def apply_global_styles(self):
        """Apply global CSS styles and theme"""
        # Load main CSS
        css_content = self.theme_manager.generate_adaptive_css()
        st.markdown(css_content, unsafe_allow_html=True)
        
        # Inject theme detection script
        theme_detector = self.theme_manager.inject_theme_detector()
        st.markdown(theme_detector, unsafe_allow_html=True)
        
        # Load additional component CSS
        additional_css = self._get_component_css()
        st.markdown(additional_css, unsafe_allow_html=True)
    
    def _get_component_css(self) -> str:
        """Combine CSS from all components"""
        css_parts = [
            self.header.get_header_css(),
            self.sidebar.get_sidebar_css(),
            self.about_section.get_about_css(),
            self.skills_section.get_skills_css(),
            self.projects_section.get_projects_css(),
            self.github_stats_section.get_github_stats_css(),
            self.contact_section.get_contact_css()
        ]
        return "\n".join(css_parts)
    
    def run(self):
        """Main application execution"""
        try:
            # Track application start
            performance_monitor.track_page_load()
            self.settings.update_visit_count()
            
            # Apply styling
            self.apply_global_styles()
            
            # Render header
            self.header.render()
            
            # Show notifications
            self.notification_manager.show_notifications()
            
            # Render sidebar and get selected page
            selected_page = self.sidebar.render()
            
            # Render main content based on selection
            self.render_main_content(selected_page)
            
            # Render footer
            self.render_footer()
            
        except Exception as e:
            self.handle_application_error(e)
    
    def render_main_content(self, selected_page: str):
        """Render main content based on selected page"""
        try:
            if selected_page == "About Me":
                self.about_section.render()
                # Optionally render additional sections
                if st.session_state.get('user_preferences', {}).get('show_extended_about', False):
                    self.about_section.render_achievements()
                    self.about_section.render_timeline()
            
            elif selected_page == "Skills & Technologies":
                self.skills_section.render()
                self.skills_section.render_learning_roadmap()
            
            elif selected_page == "Projects":
                self.projects_section.render()
            
            elif selected_page == "GitHub Stats":
                self.github_stats_section.render()
            
            elif selected_page == "Contact":
                self.contact_section.render()
                self.contact_section.render_faq_section()
                
                # Show contact stats in debug mode
                if self.settings.is_development_mode():
                    self.contact_section.render_contact_stats()
            
            else:
                # Fallback to About Me
                self.about_section.render()
                
        except Exception as e:
            st.error("An error occurred while loading the selected section.")
            if self.settings.is_development_mode():
                st.exception(e)
    
    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        
        # Performance stats in development mode
        if self.settings.is_development_mode():
            with st.expander("🔧 Developer Information", expanded=False):
                self.render_debug_info()
        
        # Main footer
        visit_count = st.session_state.get('visit_count', 0)
        current_year = 2024  # Could be made dynamic
        
        footer_html = f"""
        <div class="footer">
            <p>© {current_year} {DEVELOPER_NAME} | Visit #{visit_count}</p>
            <p>Built with ❤️ using Streamlit | Refactored for modern architecture</p>
            <p>
                <small>
                    Theme: {st.session_state.get('theme_preference', 'auto').title()} | 
                    Version: 2.0 | 
                    Last Updated: January 2024
                </small>
            </p>
        </div>
        """
        
        st.markdown(footer_html, unsafe_allow_html=True)
    
    def render_debug_info(self):
        """Render debug information for development"""
        # Performance metrics
        perf_stats = performance_monitor.get_performance_stats()
        st.json(perf_stats)
        
        # Session state info
        st.write("**Session State:**")
        session_info = {
            'visit_count': st.session_state.get('visit_count', 0),
            'theme_preference': st.session_state.get('theme_preference', 'auto'),
            'user_preferences': st.session_state.get('user_preferences', {}),
            'form_submissions': st.session_state.get('form_submissions', 0)
        }
        st.json(session_info)
        
        # Environment info
        st.write("**Environment:**")
        env_info = {
            'STREAMLIT_ENV': os.getenv('STREAMLIT_ENV', 'not set'),
            'DEBUG_MODE': os.getenv('DEBUG_MODE', 'not set'),
            'GITHUB_TOKEN': 'set' if os.getenv('GITHUB_TOKEN') else 'not set'
        }
        st.json(env_info)
    
    def handle_application_error(self, error: Exception):
        """Handle application-level errors gracefully"""
        st.error("An unexpected error occurred in the application.")
        
        if self.settings.is_development_mode():
            st.exception(error)
        else:
            st.info("Please try refreshing the page. If the problem persists, please contact support.")
        
        # Log error for debugging
        if hasattr(st.session_state, 'error_log'):
            st.session_state.error_log.append({
                'error': str(error),
                'context': 'application_level',
                'timestamp': st.session_state.get('current_time', 'unknown')
            })

def main():
    """Application entry point"""
    try:
        # Initialize and run the portfolio application
        app = PortfolioApp()
        app.run()
        
    except Exception as e:
        # Fallback error handling
        st.error("Critical error: Unable to initialize the application.")
        st.exception(e)

if __name__ == "__main__":
    main()