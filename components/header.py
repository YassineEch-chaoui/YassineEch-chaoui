"""
Header component for the portfolio application
"""
import streamlit as st
from components.base import BaseComponent
from config.constants import DEVELOPER_NAME, DEVELOPER_TAGLINE

class HeaderComponent(BaseComponent):
    """Renders the main header with title and navigation"""
    
    def __init__(self, theme_manager=None):
        super().__init__(theme_manager)
    
    def render(self) -> None:
        """Render the header component"""
        try:
            self.apply_theme()
            self._render_main_header()
            self._render_theme_toggle()
        except Exception as e:
            self.handle_error(e, "header rendering")
    
    def _render_main_header(self) -> None:
        """Render the main header content"""
        header_html = f"""
        <div{self.add_animation_class()}>
            <h1 class="main-header">💻 {DEVELOPER_NAME}</h1>
            <p class="main-subtitle">{DEVELOPER_TAGLINE}</p>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    
    def _render_theme_toggle(self) -> None:
        """Render theme toggle button"""
        # Create a small theme toggle in the sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎨 Theme")
            
            current_theme = st.session_state.get('theme_preference', 'auto')
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("☀️", key="light_theme", help="Light theme"):
                    st.session_state.theme_preference = 'light'
                    st.rerun()
            
            with col2:
                if st.button("🌙", key="dark_theme", help="Dark theme"):
                    st.session_state.theme_preference = 'dark'
                    st.rerun()
            
            with col3:
                if st.button("🔄", key="auto_theme", help="Auto theme"):
                    st.session_state.theme_preference = 'auto'
                    st.rerun()
            
            # Show current theme
            theme_status = {
                'light': "☀️ Light",
                'dark': "🌙 Dark", 
                'auto': "🔄 Auto"
            }
            st.caption(f"Current: {theme_status.get(current_theme, 'Auto')}")
    
    def render_breadcrumb(self, current_page: str) -> None:
        """Render breadcrumb navigation"""
        breadcrumb_html = f"""
        <div class="breadcrumb">
            <span class="breadcrumb-item">
                <a href="#" onclick="return false;">Home</a>
            </span>
            <span class="breadcrumb-separator">›</span>
            <span class="breadcrumb-item active">{current_page}</span>
        </div>
        """
        st.markdown(breadcrumb_html, unsafe_allow_html=True)
    
    def render_announcement(self, message: str, type: str = "info") -> None:
        """Render announcement banner"""
        if not message:
            return
        
        announcement_class = f"announcement announcement-{type}"
        announcement_html = f"""
        <div class="{announcement_class}">
            <div class="announcement-content">
                {message}
            </div>
        </div>
        """
        st.markdown(announcement_html, unsafe_allow_html=True)
    
    def get_header_css(self) -> str:
        """Get additional CSS for header styling"""
        return """
        <style>
        .breadcrumb {
            display: flex;
            align-items: center;
            margin: 1rem 0;
            padding: 0.5rem 0;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }
        
        .breadcrumb-item a {
            color: var(--secondary-color);
            text-decoration: none;
        }
        
        .breadcrumb-item.active {
            color: var(--text-primary);
            font-weight: 500;
        }
        
        .breadcrumb-separator {
            margin: 0 0.5rem;
            color: var(--text-secondary);
        }
        
        .announcement {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
            background: var(--surface-color);
        }
        
        .announcement-info {
            border-left-color: var(--secondary-color);
        }
        
        .announcement-warning {
            border-left-color: #ffc107;
        }
        
        .announcement-error {
            border-left-color: #dc3545;
        }
        
        .announcement-content {
            color: var(--text-primary);
            font-weight: 500;
        }
        </style>
        """