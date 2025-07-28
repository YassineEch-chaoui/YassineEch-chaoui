"""
Skills & Technologies section component
"""
import streamlit as st
from components.base import BaseComponent
from config.constants import SKILLS_CATEGORIES
from utils.cache_manager import cached_function

class SkillsSection(BaseComponent):
    """Renders the Skills & Technologies section"""
    
    def __init__(self, theme_manager=None):
        super().__init__(theme_manager)
    
    def render(self) -> None:
        """Render the skills section"""
        try:
            self._render_section_header()
            self._render_skills_overview()
            self._render_skills_categories()
            self._render_skill_level_info()
        except Exception as e:
            self.handle_error(e, "skills section rendering")
    
    def _render_section_header(self) -> None:
        """Render section header"""
        st.markdown('<h2 class="section-header">🛠️ Skills & Technologies</h2>', unsafe_allow_html=True)
    
    def _render_skills_overview(self) -> None:
        """Render skills overview statistics"""
        total_skills = sum(len(skills) for skills in SKILLS_CATEGORIES.values())
        categories_count = len(SKILLS_CATEGORIES)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.create_metric_card("Total Skills", str(total_skills))
        
        with col2:
            self.create_metric_card("Categories", str(categories_count))
        
        with col3:
            self.create_metric_card("Experience", "3+ Years")
        
        with col4:
            self.create_metric_card("Learning", "Always")
        
        st.markdown("---")
    
    def _render_skills_categories(self) -> None:
        """Render skills organized by categories"""
        # Create tabs for different views
        tab1, tab2 = st.tabs(["📋 By Category", "⭐ Featured Skills"])
        
        with tab1:
            self._render_category_view()
        
        with tab2:
            self._render_featured_skills()
    
    def _render_category_view(self) -> None:
        """Render skills grouped by categories"""
        for category, skills in SKILLS_CATEGORIES.items():
            with st.container():
                # Category header
                category_html = f"""
                <div{self.add_animation_class()}>
                    <h3 style="
                        color: var(--primary-color);
                        margin: 2rem 0 1rem 0;
                        padding-bottom: 0.5rem;
                        border-bottom: 2px solid var(--secondary-color);
                        font-weight: 600;
                    ">
                        {self._get_category_icon(category)} {category}
                    </h3>
                </div>
                """
                st.markdown(category_html, unsafe_allow_html=True)
                
                # Skills badges
                skills_html = f"""
                <div{self.add_animation_class()} style="margin-bottom: 2rem;">
                """
                
                for skill in skills:
                    skill_level = self._get_skill_level(skill)
                    badge_class = self._get_skill_badge_class(skill_level)
                    
                    skills_html += f"""
                    <span class="tech-badge {badge_class}" title="{skill} - {skill_level}">
                        {skill}
                    </span>
                    """
                
                skills_html += "</div>"
                st.markdown(skills_html, unsafe_allow_html=True)
    
    def _render_featured_skills(self) -> None:
        """Render featured/highlighted skills"""
        featured_skills = self._get_featured_skills()
        
        st.markdown("### 🌟 Most Proficient")
        
        # Create progress bars for featured skills
        for skill_data in featured_skills:
            skill_name = skill_data['name']
            proficiency = skill_data['proficiency']
            category = skill_data['category']
            
            # Create a skill card with progress
            skill_card_html = f"""
            <div class="skill-card"{self.add_animation_class()}>
                <div class="skill-header">
                    <h4>{skill_name}</h4>
                    <span class="skill-category">{category}</span>
                </div>
                <div class="skill-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {proficiency}%"></div>
                    </div>
                    <span class="progress-text">{proficiency}%</span>
                </div>
            </div>
            """
            st.markdown(skill_card_html, unsafe_allow_html=True)
    
    def _render_skill_level_info(self) -> None:
        """Render skill level legend"""
        with st.expander("📖 Skill Level Guide", expanded=False):
            levels_html = """
            <div class="skill-levels">
                <div class="level-item">
                    <span class="tech-badge expert">Expert</span>
                    <span>Advanced proficiency, can mentor others</span>
                </div>
                <div class="level-item">
                    <span class="tech-badge advanced">Advanced</span>
                    <span>Highly proficient, complex project experience</span>
                </div>
                <div class="level-item">
                    <span class="tech-badge intermediate">Intermediate</span>
                    <span>Good working knowledge, moderate experience</span>
                </div>
                <div class="level-item">
                    <span class="tech-badge beginner">Beginner</span>
                    <span>Basic knowledge, learning actively</span>
                </div>
            </div>
            """
            st.markdown(levels_html, unsafe_allow_html=True)
    
    def _get_category_icon(self, category: str) -> str:
        """Get icon for skill category"""
        icons = {
            "Programming Languages": "💻",
            "Web Technologies": "🌐",
            "Databases": "🗄️",
            "Cloud & DevOps": "☁️",
            "Tools & Others": "🔧"
        }
        return icons.get(category, "📚")
    
    @cached_function(ttl=3600, key_prefix="skill_level")
    def _get_skill_level(self, skill: str) -> str:
        """Get skill proficiency level (could be enhanced with real data)"""
        # This could be connected to a database or API in the future
        skill_levels = {
            # Programming Languages
            "Python": "Expert",
            "JavaScript": "Advanced", 
            "TypeScript": "Advanced",
            "Java": "Intermediate",
            "C#": "Intermediate",
            "C++": "Intermediate",
            
            # Web Technologies
            "HTML5": "Expert",
            "CSS3": "Expert",
            "React": "Advanced",
            "Flask": "Advanced",
            "Django": "Advanced",
            
            # Databases
            "MySQL": "Advanced",
            "MongoDB": "Intermediate",
            
            # Cloud & DevOps
            "Docker": "Advanced",
            "Git": "Expert",
            "Azure": "Intermediate",
            
            # Default for others
        }
        return skill_levels.get(skill, "Intermediate")
    
    def _get_skill_badge_class(self, level: str) -> str:
        """Get CSS class for skill level"""
        classes = {
            "Expert": "expert",
            "Advanced": "advanced", 
            "Intermediate": "intermediate",
            "Beginner": "beginner"
        }
        return classes.get(level, "intermediate")
    
    def _get_featured_skills(self) -> list:
        """Get list of featured skills with proficiency"""
        return [
            {"name": "Python", "proficiency": 95, "category": "Programming"},
            {"name": "JavaScript", "proficiency": 90, "category": "Programming"},
            {"name": "React", "proficiency": 85, "category": "Web"},
            {"name": "Docker", "proficiency": 80, "category": "DevOps"},
            {"name": "Git", "proficiency": 95, "category": "Tools"},
            {"name": "MySQL", "proficiency": 85, "category": "Database"}
        ]
    
    def render_learning_roadmap(self) -> None:
        """Render current learning goals"""
        with st.expander("🎯 Currently Learning", expanded=False):
            learning_items = [
                {"skill": "Kubernetes", "progress": 60, "target": "Q2 2024"},
                {"skill": "Machine Learning", "progress": 40, "target": "Q3 2024"},
                {"skill": "GraphQL", "progress": 30, "target": "Q4 2024"}
            ]
            
            for item in learning_items:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"📚 {item['skill']}")
                
                with col2:
                    st.progress(item['progress'] / 100)
                    st.caption(f"{item['progress']}%")
                
                with col3:
                    st.caption(f"Target: {item['target']}")
    
    def get_skills_css(self) -> str:
        """Get additional CSS for skills section"""
        return """
        <style>
        .tech-badge.expert {
            background: linear-gradient(135deg, #28a745, #20c997);
        }
        
        .tech-badge.advanced {
            background: linear-gradient(135deg, #007bff, #6f42c1);
        }
        
        .tech-badge.intermediate {
            background: linear-gradient(135deg, #ffc107, #fd7e14);
        }
        
        .tech-badge.beginner {
            background: linear-gradient(135deg, #6c757d, #495057);
        }
        
        .skill-card {
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        
        .skill-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .skill-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .skill-header h4 {
            margin: 0;
            color: var(--text-primary);
        }
        
        .skill-category {
            background: var(--primary-color);
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.7rem;
        }
        
        .skill-progress {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .progress-bar {
            flex: 1;
            background: var(--border-color);
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        .progress-text {
            font-size: 0.8rem;
            color: var(--text-secondary);
            min-width: 35px;
        }
        
        .skill-levels {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .level-item {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .level-item span:last-child {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .skill-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
        }
        </style>
        """