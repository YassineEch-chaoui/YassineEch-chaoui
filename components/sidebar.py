"""
Sidebar navigation component
"""
import streamlit as st
from components.base import BaseComponent
from config.constants import NAVIGATION_ITEMS

class SidebarComponent(BaseComponent):
    """Renders the sidebar navigation"""
    
    def __init__(self, theme_manager=None):
        super().__init__(theme_manager)
    
    def render(self) -> str:
        """
        Render the sidebar and return selected page
        Returns: Selected page name
        """
        try:
            with st.sidebar:
                self._render_navigation_header()
                selected_page = self._render_navigation_menu()
                self._render_sidebar_footer()
                self._render_user_preferences()
                return selected_page
        except Exception as e:
            self.handle_error(e, "sidebar rendering")
            return NAVIGATION_ITEMS[0]  # Return first item as default
    
    def _render_navigation_header(self) -> None:
        """Render the navigation header in sidebar"""
        st.markdown("# 🧭 Navigation")
        st.markdown("---")
    
    def _render_navigation_menu(self) -> str:
        """Render the main navigation menu"""
        # Enhanced navigation with icons
        nav_items_with_icons = {
            "About Me": "👨‍💻",
            "Skills & Technologies": "🛠️", 
            "Projects": "🚀",
            "GitHub Stats": "📊",
            "Contact": "📬"
        }
        
        # Create formatted options
        formatted_options = [
            f"{nav_items_with_icons.get(item, '•')} {item}" 
            for item in NAVIGATION_ITEMS
        ]
        
        # Get current selection with persistence
        current_page_key = 'current_page'
        if current_page_key not in st.session_state:
            st.session_state[current_page_key] = NAVIGATION_ITEMS[0]
        
        # Find current index
        try:
            current_index = NAVIGATION_ITEMS.index(st.session_state[current_page_key])
        except ValueError:
            current_index = 0
        
        # Radio button selection
        selected_formatted = st.radio(
            "Choose a section:",
            formatted_options,
            index=current_index,
            key="nav_radio"
        )
        
        # Extract the actual page name (remove icon and space)
        selected_page = selected_formatted.split(" ", 1)[1]
        st.session_state[current_page_key] = selected_page
        
        return selected_page
    
    def _render_sidebar_footer(self) -> None:
        """Render sidebar footer with additional info"""
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        
        # Visit counter
        visit_count = st.session_state.get('visit_count', 0)
        st.metric("Visits", visit_count)
        
        # Cache stats if available
        cache_stats = self.cache_manager.get_cache_stats()
        if cache_stats['total_items'] > 0:
            st.metric("Cache Items", cache_stats['total_items'])
            st.metric("Cache Hit Ratio", f"{cache_stats['cache_hit_ratio']:.2%}")
        
        st.markdown("---")
        
        # Links section
        st.markdown("### 🔗 Quick Links")
        st.markdown("""
        - [GitHub Profile](https://github.com/YassineEch-chaoui)
        - [Portfolio Source](https://github.com/YassineEch-chaoui/YassineEch-chaoui)
        """)
    
    def _render_user_preferences(self) -> None:
        """Render user preferences section"""
        st.markdown("---")
        st.markdown("### ⚙️ Preferences")
        
        # Get current preferences
        preferences = st.session_state.get('user_preferences', {})
        
        # Animation toggle
        animations_enabled = st.checkbox(
            "Enable animations",
            value=preferences.get('animations_enabled', True),
            key="animations_toggle"
        )
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox(
            "Auto-refresh data",
            value=preferences.get('auto_refresh', False),
            key="auto_refresh_toggle"
        )
        
        # Compact mode toggle
        compact_mode = st.checkbox(
            "Compact mode",
            value=preferences.get('compact_mode', False),
            key="compact_mode_toggle"
        )
        
        # Update preferences
        st.session_state.user_preferences = {
            'animations_enabled': animations_enabled,
            'auto_refresh': auto_refresh,
            'compact_mode': compact_mode
        }
        
        # Cache management
        if st.button("🗑️ Clear Cache", help="Clear all cached data"):
            self.cache_manager.clear_all_cache()
            st.success("Cache cleared!")
            st.rerun()
    
    def render_progress_indicator(self, sections_completed: int, total_sections: int) -> None:
        """Render progress indicator for portfolio completion"""
        if total_sections > 0:
            progress = sections_completed / total_sections
            st.progress(progress)
            st.caption(f"Portfolio: {sections_completed}/{total_sections} sections complete")
    
    def render_sidebar_announcement(self, message: str, type: str = "info") -> None:
        """Render announcement in sidebar"""
        if not message:
            return
        
        announcement_types = {
            "info": ("ℹ️", "#17a2b8"),
            "warning": ("⚠️", "#ffc107"),
            "success": ("✅", "#28a745"),
            "error": ("❌", "#dc3545")
        }
        
        icon, color = announcement_types.get(type, announcement_types["info"])
        
        st.markdown(f"""
        <div style="
            background-color: rgba({color[1:]}, 0.1);
            border: 1px solid {color};
            border-radius: 8px;
            padding: 0.8rem;
            margin: 1rem 0;
        ">
            <div style="color: {color}; font-weight: bold;">
                {icon} {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def get_sidebar_css(self) -> str:
        """Get additional CSS for sidebar styling"""
        return """
        <style>
        /* Sidebar enhancements */
        .css-1d391kg {
            background: var(--surface-color);
            border-right: 1px solid var(--border-color);
        }
        
        /* Radio button styling */
        .stRadio > div > label > div > div {
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.5rem;
            margin: 0.2rem 0;
            transition: all 0.3s ease;
        }
        
        .stRadio > div > label > div > div:hover {
            border-color: var(--primary-color);
            background-color: rgba(255, 107, 107, 0.1);
        }
        
        /* Checkbox styling */
        .stCheckbox > label {
            color: var(--text-primary);
            font-size: 0.9rem;
        }
        
        /* Metric styling in sidebar */
        .metric-container {
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.5rem;
            margin: 0.5rem 0;
            text-align: center;
        }
        
        /* Quick links styling */
        .sidebar-links a {
            color: var(--secondary-color);
            text-decoration: none;
            font-size: 0.9rem;
        }
        
        .sidebar-links a:hover {
            color: var(--primary-color);
        }
        </style>
        """