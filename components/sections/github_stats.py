"""
GitHub Statistics section component
"""
import streamlit as st
import requests
from components.base import BaseComponent
from config.constants import (
    GITHUB_API_URL, GITHUB_USERNAME, GITHUB_API_TIMEOUT,
    ERROR_MESSAGES, LOADING_MESSAGES
)
from utils.cache_manager import cached_function

class GitHubStatsSection(BaseComponent):
    """Renders the GitHub Statistics section"""
    
    def __init__(self, theme_manager=None):
        super().__init__(theme_manager)
    
    def render(self) -> None:
        """Render the GitHub stats section"""
        try:
            self._render_section_header()
            self._render_user_stats()
            self._render_contribution_graphs()
            self._render_activity_timeline()
        except Exception as e:
            self.handle_error(e, "GitHub stats section rendering")
    
    def _render_section_header(self) -> None:
        """Render section header"""
        st.markdown('<h2 class="section-header">📊 GitHub Statistics</h2>', unsafe_allow_html=True)
    
    def _render_user_stats(self) -> None:
        """Render basic GitHub user statistics"""
        with st.spinner(LOADING_MESSAGES['github_stats']):
            user_data = self._get_github_user_data()
        
        if not user_data:
            self._render_stats_error()
            return
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.create_metric_card(
                "Public Repos", 
                user_data.get('public_repos', 0),
                self._calculate_repo_delta()
            )
        
        with col2:
            self.create_metric_card(
                "Followers", 
                user_data.get('followers', 0)
            )
        
        with col3:
            self.create_metric_card(
                "Following", 
                user_data.get('following', 0)
            )
        
        with col4:
            self.create_metric_card(
                "Public Gists", 
                user_data.get('public_gists', 0)
            )
        
        # Additional info
        self._render_user_info(user_data)
    
    def _render_user_info(self, user_data: dict) -> None:
        """Render additional user information"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Account info
            info_html = f"""
            <div class="github-info-card"{self.add_animation_class()}>
                <h4>👤 Account Information</h4>
                <div class="info-item">
                    <strong>Username:</strong> {user_data.get('login', 'N/A')}
                </div>
                <div class="info-item">
                    <strong>Account Type:</strong> {user_data.get('type', 'User')}
                </div>
                <div class="info-item">
                    <strong>Member Since:</strong> {self._format_date(user_data.get('created_at', ''))}
                </div>
                <div class="info-item">
                    <strong>Last Updated:</strong> {self._format_date(user_data.get('updated_at', ''))}
                </div>
            </div>
            """
            st.markdown(info_html, unsafe_allow_html=True)
        
        with col2:
            # Profile links
            links_html = f"""
            <div class="github-info-card"{self.add_animation_class()}>
                <h4>🔗 Profile Links</h4>
                <div class="info-item">
                    <a href="{user_data.get('html_url', '#')}" target="_blank" class="profile-link">
                        🐙 GitHub Profile
                    </a>
                </div>
                {self._render_blog_link(user_data.get('blog', ''))}
                {self._render_twitter_link(user_data.get('twitter_username', ''))}
                <div class="info-item">
                    <strong>Location:</strong> {user_data.get('location', 'Not specified')}
                </div>
            </div>
            """
            st.markdown(links_html, unsafe_allow_html=True)
    
    def _render_contribution_graphs(self) -> None:
        """Render GitHub contribution graphs using external services"""
        st.markdown("---")
        st.markdown("### 📈 Contribution Statistics")
        
        # Use GitHub README stats
        tab1, tab2 = st.tabs(["📊 Overall Stats", "📋 Language Stats"])
        
        with tab1:
            self._render_github_readme_stats()
        
        with tab2:
            self._render_language_stats()
    
    def _render_github_readme_stats(self) -> None:
        """Render GitHub README stats"""
        try:
            # GitHub stats card
            stats_url = f"https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&theme=radical&hide_border=false&include_all_commits=true&count_private=false"
            
            # Check current theme preference
            theme_preference = st.session_state.get('theme_preference', 'auto')
            
            if theme_preference == 'dark':
                stats_url += "&theme=dark"
            elif theme_preference == 'light':
                stats_url += "&theme=default"
            else:
                stats_url += "&theme=radical"  # Default theme
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(
                    stats_url,
                    caption="GitHub Statistics",
                    use_column_width=True
                )
        
        except Exception as e:
            st.error("Unable to load GitHub statistics visualization")
            self.handle_error(e, "GitHub stats visualization")
    
    def _render_language_stats(self) -> None:
        """Render language statistics"""
        try:
            # Language stats
            theme_preference = st.session_state.get('theme_preference', 'auto')
            
            lang_stats_url = f"https://github-readme-stats.vercel.app/api/top-langs/?username={GITHUB_USERNAME}&layout=compact&hide_border=false&include_all_commits=true&count_private=false"
            
            if theme_preference == 'dark':
                lang_stats_url += "&theme=dark"
            elif theme_preference == 'light':
                lang_stats_url += "&theme=default"
            else:
                lang_stats_url += "&theme=radical"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(
                    lang_stats_url,
                    caption="Most Used Languages",
                    use_column_width=True
                )
        
        except Exception as e:
            st.error("Unable to load language statistics visualization")
            self.handle_error(e, "language stats visualization")
    
    def _render_activity_timeline(self) -> None:
        """Render recent activity timeline"""
        st.markdown("---")
        st.markdown("### 🕒 Recent Activity")
        
        with st.expander("📅 Activity Timeline", expanded=False):
            recent_events = self._get_recent_events()
            
            if recent_events:
                for event in recent_events[:10]:  # Show last 10 events
                    self._render_activity_item(event)
            else:
                st.info("No recent activity data available")
    
    @cached_function(ttl=1800, key_prefix="github_user")
    def _get_github_user_data(self) -> dict:
        """
        Fetch GitHub user data with caching
        Returns user data dictionary
        """
        try:
            self.performance_monitor.track_api_call()
            
            headers = {}
            
            # Add authentication if available
            github_token = st.session_state.get('github_token', '')
            if github_token:
                headers['Authorization'] = f"token {github_token}"
            
            response = requests.get(
                f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}",
                headers=headers,
                timeout=GITHUB_API_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                st.warning("GitHub API rate limit exceeded")
                return {}
            else:
                st.error(f"GitHub API error: {response.status_code}")
                return {}
                
        except requests.RequestException as e:
            self.handle_error(e, "GitHub user API request")
            return {}
        except Exception as e:
            self.handle_error(e, "fetching GitHub user data")
            return {}
    
    @cached_function(ttl=3600, key_prefix="github_events")
    def _get_recent_events(self) -> list:
        """
        Fetch recent GitHub events
        Returns list of events
        """
        try:
            response = requests.get(
                f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/events/public",
                timeout=GITHUB_API_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            self.handle_error(e, "fetching GitHub events")
            return []
    
    def _render_activity_item(self, event: dict) -> None:
        """Render individual activity item"""
        try:
            event_type = event.get('type', 'Unknown')
            created_at = self._format_date(event.get('created_at', ''))
            repo_name = event.get('repo', {}).get('name', 'Unknown')
            
            # Get event icon and description
            icon, description = self._get_event_display_info(event_type, event)
            
            activity_html = f"""
            <div class="activity-item">
                <div class="activity-icon">{icon}</div>
                <div class="activity-content">
                    <div class="activity-description">{description}</div>
                    <div class="activity-meta">
                        <span class="activity-repo">{repo_name}</span>
                        <span class="activity-time">{created_at}</span>
                    </div>
                </div>
            </div>
            """
            
            st.markdown(activity_html, unsafe_allow_html=True)
            
        except Exception as e:
            self.handle_error(e, "rendering activity item")
    
    def _get_event_display_info(self, event_type: str, event: dict) -> tuple:
        """Get display icon and description for event type"""
        event_info = {
            'PushEvent': ('📝', 'Pushed commits'),
            'CreateEvent': ('🆕', 'Created repository/branch'),
            'ForkEvent': ('🍴', 'Forked repository'),
            'WatchEvent': ('⭐', 'Starred repository'),
            'IssuesEvent': ('🐛', 'Opened/closed issue'),
            'PullRequestEvent': ('🔄', 'Created/merged pull request'),
            'DeleteEvent': ('🗑️', 'Deleted branch/tag'),
            'ReleaseEvent': ('🚀', 'Published release'),
            'PublicEvent': ('🌍', 'Made repository public')
        }
        
        icon, base_description = event_info.get(event_type, ('📌', 'Activity'))
        
        # Add more specific information based on event type
        if event_type == 'PushEvent':
            commits_count = len(event.get('payload', {}).get('commits', []))
            description = f"{base_description} ({commits_count} commit{'s' if commits_count != 1 else ''})"
        else:
            description = base_description
        
        return icon, description
    
    def _render_stats_error(self) -> None:
        """Render error message for stats loading failure"""
        st.error(ERROR_MESSAGES['github_api_error'])
        
        # Show cached data if available
        cached_data = self.cache_manager.get_cached_data("github_user")
        if cached_data:
            st.info("Showing cached data from previous session")
            self._render_user_stats_from_cache(cached_data)
    
    def _render_user_stats_from_cache(self, cached_data: dict) -> None:
        """Render user stats from cached data"""
        # Simple fallback display
        st.metric("Public Repos", cached_data.get('public_repos', 'N/A'))
        st.metric("Followers", cached_data.get('followers', 'N/A'))
    
    def _render_blog_link(self, blog_url: str) -> str:
        """Render blog link if available"""
        if blog_url and self.security_validator.is_safe_url(blog_url):
            return f"""
            <div class="info-item">
                <a href="{blog_url}" target="_blank" class="profile-link">
                    🌐 Blog/Website
                </a>
            </div>
            """
        return ""
    
    def _render_twitter_link(self, twitter_username: str) -> str:
        """Render Twitter link if available"""
        if twitter_username:
            twitter_url = f"https://twitter.com/{twitter_username}"
            return f"""
            <div class="info-item">
                <a href="{twitter_url}" target="_blank" class="profile-link">
                    🐦 Twitter
                </a>
            </div>
            """
        return ""
    
    def _format_date(self, date_string: str) -> str:
        """Format ISO date string to readable format"""
        if not date_string:
            return "Unknown"
        
        try:
            from datetime import datetime
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date_obj.strftime("%b %d, %Y")
        except:
            return "Unknown"
    
    def _calculate_repo_delta(self) -> str:
        """Calculate repository count change (placeholder)"""
        # This could be enhanced to track changes over time
        return None
    
    def get_github_stats_css(self) -> str:
        """Get additional CSS for GitHub stats section"""
        return """
        <style>
        .github-info-card {
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .github-info-card h4 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .info-item {
            margin: 0.5rem 0;
            color: var(--text-primary);
            font-size: 0.9rem;
        }
        
        .profile-link {
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        
        .profile-link:hover {
            color: var(--primary-color);
        }
        
        .activity-item {
            display: flex;
            align-items: flex-start;
            margin: 1rem 0;
            padding: 0.8rem;
            background: var(--surface-color);
            border-radius: 8px;
            border-left: 3px solid var(--secondary-color);
        }
        
        .activity-icon {
            font-size: 1.2rem;
            margin-right: 1rem;
            flex-shrink: 0;
        }
        
        .activity-content {
            flex: 1;
        }
        
        .activity-description {
            color: var(--text-primary);
            font-weight: 500;
            margin-bottom: 0.3rem;
        }
        
        .activity-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }
        
        .activity-repo {
            font-weight: 500;
        }
        
        @media (max-width: 768px) {
            .github-info-card {
                padding: 0.8rem;
            }
            
            .activity-meta {
                flex-direction: column;
                gap: 0.2rem;
            }
        }
        </style>
        """