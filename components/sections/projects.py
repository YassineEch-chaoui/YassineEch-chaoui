"""
Projects section component with GitHub integration
"""
import streamlit as st
import requests
from datetime import datetime
from components.base import BaseComponent
from config.constants import (
    GITHUB_API_URL, GITHUB_USERNAME, GITHUB_API_TIMEOUT, 
    MAX_REPOS_DISPLAY, ERROR_MESSAGES, LOADING_MESSAGES
)
from utils.cache_manager import cached_function
from utils.validators import SecurityValidator

class ProjectsSection(BaseComponent):
    """Renders the Projects section with GitHub integration"""
    
    def __init__(self, theme_manager=None):
        super().__init__(theme_manager)
    
    def render(self) -> None:
        """Render the projects section"""
        try:
            self._render_section_header()
            self._render_projects_overview()
            self._render_github_projects()
        except Exception as e:
            self.handle_error(e, "projects section rendering")
    
    def _render_section_header(self) -> None:
        """Render section header"""
        st.markdown('<h2 class="section-header">🚀 Projects</h2>', unsafe_allow_html=True)
    
    def _render_projects_overview(self) -> None:
        """Render projects overview with filters"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("### Featured Projects from GitHub")
            st.caption("Showcasing my latest work and contributions")
        
        with col2:
            # Refresh button
            if st.button("🔄 Refresh", help="Refresh project data"):
                self._clear_projects_cache()
                st.rerun()
        
        with col3:
            # Filter options
            show_all = st.checkbox("Show all repos", value=False)
            st.session_state['show_all_repos'] = show_all
    
    def _render_github_projects(self) -> None:
        """Render projects from GitHub"""
        with st.spinner(LOADING_MESSAGES['github_repos']):
            repos = self._get_github_repos()
        
        if not repos:
            self._render_no_projects_message()
            return
        
        # Filter and sort repositories
        filtered_repos = self._filter_repositories(repos)
        
        if not filtered_repos:
            st.info("No projects match the current filters.")
            return
        
        # Render project grid
        self._render_project_grid(filtered_repos)
        
        # Show additional statistics
        self._render_project_stats(repos)
    
    @cached_function(ttl=1800, key_prefix="github_repos")  # 30 minutes cache
    def _get_github_repos(self) -> list:
        """
        Fetch repositories from GitHub API with caching
        Returns list of repository data
        """
        try:
            # Track API call
            self.performance_monitor.track_api_call()
            
            headers = {}
            
            # Add authentication if token is available
            if self.cache_manager.get_cached_data("github_token"):
                headers['Authorization'] = f"token {self.cache_manager.get_cached_data('github_token')}"
            
            response = requests.get(
                f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/repos",
                headers=headers,
                timeout=GITHUB_API_TIMEOUT,
                params={
                    'sort': 'updated',
                    'direction': 'desc',
                    'per_page': 100
                }
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                # Rate limit exceeded
                st.warning("GitHub API rate limit exceeded. Showing cached data if available.")
                return []
            else:
                st.error(f"GitHub API error: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            self.handle_error(e, "GitHub API request")
            return []
        except Exception as e:
            self.handle_error(e, "fetching GitHub repositories")
            return []
    
    def _filter_repositories(self, repos: list) -> list:
        """Filter repositories based on criteria"""
        if not repos:
            return []
        
        show_all = st.session_state.get('show_all_repos', False)
        
        # Filter out forks and repositories without descriptions (unless show_all is True)
        if show_all:
            filtered = repos
        else:
            filtered = [
                repo for repo in repos 
                if not repo.get('fork', False) and repo.get('description')
            ]
        
        # Sort by last updated
        filtered.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        
        # Limit number of repositories
        if not show_all:
            filtered = filtered[:MAX_REPOS_DISPLAY]
        
        return filtered
    
    def _render_project_grid(self, repos: list) -> None:
        """Render projects in a grid layout"""
        # Calculate number of columns based on screen size
        compact_mode = st.session_state.get('user_preferences', {}).get('compact_mode', False)
        cols_per_row = 1 if compact_mode else 2
        
        # Group repositories into rows
        for i in range(0, len(repos), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                repo_index = i + j
                if repo_index < len(repos):
                    with col:
                        self._render_project_card(repos[repo_index])
    
    def _render_project_card(self, repo: dict) -> None:
        """Render individual project card"""
        try:
            # Sanitize repository data
            repo_name = self.validator.sanitize_input(repo.get('name', 'Unknown'))
            repo_description = self.validator.sanitize_input(repo.get('description', 'No description available'))
            repo_language = self.validator.sanitize_input(repo.get('language', 'N/A'))
            
            # Validate URL
            repo_url = repo.get('html_url', '')
            if not SecurityValidator().is_safe_url(repo_url):
                repo_url = '#'
            
            # Format dates
            updated_at = self._format_date(repo.get('updated_at'))
            created_at = self._format_date(repo.get('created_at'))
            
            # Build project card HTML
            card_html = f"""
            <div class="project-card"{self.add_animation_class()}>
                <div class="project-header">
                    <h3 class="project-title">
                        🔗 {repo_name}
                    </h3>
                    {self._render_language_badge(repo_language)}
                </div>
                
                <p class="project-description">{repo_description}</p>
                
                <div class="project-meta">
                    <div class="project-stats">
                        <span class="stat-item">
                            ⭐ {repo.get('stargazers_count', 0)}
                        </span>
                        <span class="stat-item">
                            🍴 {repo.get('forks_count', 0)}
                        </span>
                        <span class="stat-item">
                            👁️ {repo.get('watchers_count', 0)}
                        </span>
                    </div>
                    
                    <div class="project-dates">
                        <small>Updated: {updated_at}</small>
                        <small>Created: {created_at}</small>
                    </div>
                </div>
                
                <div class="project-actions">
                    <a href="{repo_url}" target="_blank" class="project-link">
                        View on GitHub →
                    </a>
                    {self._render_demo_link(repo)}
                </div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
        except Exception as e:
            self.handle_error(e, f"rendering project card for {repo.get('name', 'unknown')}")
    
    def _render_language_badge(self, language: str) -> str:
        """Render programming language badge"""
        if not language or language == 'N/A':
            return ""
        
        # Get color for language
        color = self._get_language_color(language)
        
        return f"""
        <span class="language-badge" style="background-color: {color};">
            {language}
        </span>
        """
    
    def _render_demo_link(self, repo: dict) -> str:
        """Render demo link if available"""
        homepage = repo.get('homepage', '')
        if homepage and SecurityValidator().is_safe_url(homepage):
            return f"""
            <a href="{homepage}" target="_blank" class="demo-link">
                🌐 Live Demo
            </a>
            """
        return ""
    
    def _render_project_stats(self, repos: list) -> None:
        """Render overall project statistics"""
        if not repos:
            return
        
        with st.expander("📊 Repository Statistics", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
            total_forks = sum(repo.get('forks_count', 0) for repo in repos)
            languages = [repo.get('language') for repo in repos if repo.get('language')]
            unique_languages = len(set(filter(None, languages)))
            
            with col1:
                self.create_metric_card("Total Repositories", len(repos))
            
            with col2:
                self.create_metric_card("Total Stars", total_stars)
            
            with col3:
                self.create_metric_card("Total Forks", total_forks)
            
            with col4:
                self.create_metric_card("Languages Used", unique_languages)
            
            # Language distribution
            if languages:
                st.markdown("#### 📈 Language Distribution")
                language_counts = {}
                for lang in languages:
                    if lang:
                        language_counts[lang] = language_counts.get(lang, 0) + 1
                
                # Create simple bar chart using HTML
                for lang, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    percentage = (count / len(languages)) * 100
                    color = self._get_language_color(lang)
                    
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
                            <span>{lang}</span>
                            <span>{count} repos ({percentage:.1f}%)</span>
                        </div>
                        <div style="background: var(--border-color); border-radius: 10px; height: 8px; overflow: hidden;">
                            <div style="background: {color}; height: 100%; width: {percentage}%; border-radius: 10px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    def _render_no_projects_message(self) -> None:
        """Render message when no projects are available"""
        st.warning("No projects found or unable to load GitHub repositories.")
        
        # Provide helpful information
        st.info("""
        This could be due to:
        - Network connectivity issues
        - GitHub API rate limiting
        - Repository privacy settings
        
        Please try refreshing the page or check back later.
        """)
    
    def _format_date(self, date_string: str) -> str:
        """Format ISO date string to readable format"""
        if not date_string:
            return "Unknown"
        
        try:
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date_obj.strftime("%b %d, %Y")
        except:
            return "Unknown"
    
    def _get_language_color(self, language: str) -> str:
        """Get color associated with programming language"""
        colors = {
            'Python': '#3776ab',
            'JavaScript': '#f7df1e',
            'TypeScript': '#3178c6',
            'Java': '#ed8b00',
            'C#': '#239120',
            'C++': '#00599c',
            'HTML': '#e34f26',
            'CSS': '#1572b6',
            'PHP': '#777bb4',
            'Ruby': '#cc342d',
            'Go': '#00add8',
            'Rust': '#000000',
            'Swift': '#fa7343',
            'Kotlin': '#7f52ff',
            'Shell': '#89e051',
            'Dockerfile': '#384d54'
        }
        return colors.get(language, '#6c757d')
    
    def _clear_projects_cache(self) -> None:
        """Clear projects-related cache"""
        cache_key = self.cache_manager.get_cache_key("github_repos", GITHUB_USERNAME)
        self.cache_manager.invalidate_cache(cache_key)
    
    def get_projects_css(self) -> str:
        """Get additional CSS for projects section"""
        return """
        <style>
        .project-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .project-title {
            color: var(--primary-color);
            margin: 0;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .language-badge {
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-left: 0.5rem;
        }
        
        .project-description {
            color: var(--text-primary);
            line-height: 1.5;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        
        .project-meta {
            margin-bottom: 1rem;
        }
        
        .project-stats {
            display: flex;
            gap: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .stat-item {
            color: var(--text-secondary);
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }
        
        .project-dates small {
            display: block;
            color: var(--text-secondary);
            font-size: 0.75rem;
            margin-bottom: 0.2rem;
        }
        
        .project-actions {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .project-link,
        .demo-link {
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            transition: color 0.3s ease;
        }
        
        .project-link:hover,
        .demo-link:hover {
            color: var(--primary-color);
        }
        
        .demo-link {
            color: var(--primary-color);
        }
        
        @media (max-width: 768px) {
            .project-header {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .project-stats {
                flex-wrap: wrap;
                gap: 0.5rem;
            }
            
            .project-actions {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
        }
        </style>
        """