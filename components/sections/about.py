"""
About Me section component
"""
import streamlit as st
from components.base import BaseComponent, ResponsiveLayout
from config.constants import ABOUT_ME_CONTENT

class AboutSection(BaseComponent):
    """Renders the About Me section"""
    
    def __init__(self, theme_manager=None):
        super().__init__(theme_manager)
    
    def render(self) -> None:
        """Render the about section"""
        try:
            self._render_section_header()
            self._render_about_content()
        except Exception as e:
            self.handle_error(e, "about section rendering")
    
    def _render_section_header(self) -> None:
        """Render section header"""
        st.markdown('<h2 class="section-header">👨‍💻 About Me</h2>', unsafe_allow_html=True)
    
    def _render_about_content(self) -> None:
        """Render the main about content"""
        # Use responsive layout
        def render_text_content():
            self._render_greeting_and_intro()
            self._render_traits()
            self._render_description()
        
        def render_image_content():
            self._render_profile_image()
        
        # Check if compact mode is enabled
        compact_mode = st.session_state.get('user_preferences', {}).get('compact_mode', False)
        
        if compact_mode:
            render_text_content()
            render_image_content()
        else:
            ResponsiveLayout.create_responsive_columns([
                render_text_content,
                render_image_content
            ], "desktop")
    
    def _render_greeting_and_intro(self) -> None:
        """Render greeting and introduction"""
        greeting_html = f"""
        <div{self.add_animation_class()}>
            <h3 style="color: var(--primary-color); margin-bottom: 1rem;">
                {ABOUT_ME_CONTENT['greeting']}
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.6; color: var(--text-primary);">
                {ABOUT_ME_CONTENT['intro']}
            </p>
        </div>
        """
        st.markdown(greeting_html, unsafe_allow_html=True)
    
    def _render_traits(self) -> None:
        """Render personality traits"""
        traits_html = f"""
        <div{self.add_animation_class()}>
            <h4 style="color: var(--secondary-color); margin: 1.5rem 0 1rem 0;">
                What drives me:
            </h4>
            <ul style="list-style: none; padding: 0;">
        """
        
        for trait in ABOUT_ME_CONTENT['traits']:
            traits_html += f"""
                <li style="
                    padding: 0.5rem 0;
                    font-size: 1rem;
                    color: var(--text-primary);
                    border-left: 3px solid var(--primary-color);
                    padding-left: 1rem;
                    margin: 0.5rem 0;
                ">
                    {trait}
                </li>
            """
        
        traits_html += """
            </ul>
        </div>
        """
        
        st.markdown(traits_html, unsafe_allow_html=True)
    
    def _render_description(self) -> None:
        """Render additional description"""
        description_html = f"""
        <div{self.add_animation_class()}>
            <p style="
                font-size: 1rem;
                line-height: 1.6;
                color: var(--text-primary);
                margin-top: 1.5rem;
                padding: 1rem;
                background: var(--surface-color);
                border-radius: 10px;
                border-left: 4px solid var(--secondary-color);
            ">
                {ABOUT_ME_CONTENT['description']}
            </p>
        </div>
        """
        st.markdown(description_html, unsafe_allow_html=True)
    
    def _render_profile_image(self) -> None:
        """Render profile image/GIF"""
        try:
            image_html = f"""
            <div{self.add_animation_class()} style="text-align: center;">
                <img 
                    src="{ABOUT_ME_CONTENT['gif_url']}" 
                    alt="Profile Animation"
                    style="
                        max-width: 100%;
                        height: auto;
                        border-radius: 15px;
                        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
                        transition: transform 0.3s ease;
                    "
                    onmouseover="this.style.transform='scale(1.05)'"
                    onmouseout="this.style.transform='scale(1)'"
                />
            </div>
            """
            st.markdown(image_html, unsafe_allow_html=True)
        except Exception as e:
            # Fallback if image fails to load
            st.info("🎨 Profile animation unavailable")
    
    def render_achievements(self) -> None:
        """Render achievements section (optional)"""
        achievements = [
            {"title": "Problem Solver", "description": "Turning challenges into opportunities"},
            {"title": "Continuous Learner", "description": "Always exploring new technologies"},
            {"title": "Team Player", "description": "Collaborating for better solutions"}
        ]
        
        st.markdown("### 🏆 Key Strengths")
        
        cols = st.columns(len(achievements))
        for col, achievement in zip(cols, achievements):
            with col:
                self.create_card(
                    content=f"""
                    <h4 style="color: var(--primary-color); margin-bottom: 0.5rem;">
                        {achievement['title']}
                    </h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">
                        {achievement['description']}
                    </p>
                    """,
                    card_class="achievement-card"
                )
    
    def render_timeline(self) -> None:
        """Render personal timeline (optional)"""
        timeline_items = [
            {"year": "2020+", "event": "Started coding journey"},
            {"year": "2021+", "event": "Exploring web development"},
            {"year": "2022+", "event": "Building complex applications"},
            {"year": "2023+", "event": "Contributing to open source"},
            {"year": "2024+", "event": "Continuous learning and growth"}
        ]
        
        with st.expander("📅 My Journey", expanded=False):
            for item in timeline_items:
                timeline_html = f"""
                <div style="
                    display: flex;
                    align-items: center;
                    margin: 1rem 0;
                    padding: 0.8rem;
                    background: var(--surface-color);
                    border-radius: 8px;
                    border-left: 3px solid var(--secondary-color);
                ">
                    <div style="
                        background: var(--primary-color);
                        color: white;
                        padding: 0.3rem 0.6rem;
                        border-radius: 15px;
                        font-weight: bold;
                        margin-right: 1rem;
                        min-width: 60px;
                        text-align: center;
                        font-size: 0.8rem;
                    ">
                        {item['year']}
                    </div>
                    <div style="color: var(--text-primary);">
                        {item['event']}
                    </div>
                </div>
                """
                st.markdown(timeline_html, unsafe_allow_html=True)
    
    def get_about_css(self) -> str:
        """Get additional CSS for about section"""
        return """
        <style>
        .achievement-card {
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .achievement-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            border-color: var(--primary-color);
        }
        
        .traits-list {
            animation: fadeInUp 0.6s ease-out;
        }
        
        @media (max-width: 768px) {
            .achievement-card {
                margin: 1rem 0;
            }
        }
        </style>
        """