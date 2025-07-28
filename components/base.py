"""
Base component class for all UI components
"""
import streamlit as st
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from utils.theme_manager import ThemeManager
from utils.validators import InputValidator, SecurityValidator
from utils.cache_manager import CacheManager, PerformanceMonitor

class BaseComponent(ABC):
    """Abstract base class for all UI components"""
    
    def __init__(self, theme_manager: ThemeManager = None):
        self.theme_manager = theme_manager or ThemeManager()
        self.cache_manager = CacheManager()
        self.performance_monitor = PerformanceMonitor()
        self.validator = InputValidator()
        self.security_validator = SecurityValidator()
    
    @abstractmethod
    def render(self) -> None:
        """Render the component"""
        pass
    
    def apply_theme(self) -> None:
        """Apply theme CSS to the component"""
        css = self.theme_manager.generate_adaptive_css()
        st.markdown(css, unsafe_allow_html=True)
    
    def show_loading(self, message: str = "Loading...") -> None:
        """Show loading spinner with message"""
        with st.spinner(message):
            pass
    
    def show_error(self, message: str, details: str = None) -> None:
        """Show error message"""
        st.error(message)
        if details and st.session_state.get('debug_mode', False):
            st.error(f"Debug details: {details}")
    
    def show_success(self, message: str) -> None:
        """Show success message"""
        st.success(message)
    
    def show_warning(self, message: str) -> None:
        """Show warning message"""
        st.warning(message)
    
    def show_info(self, message: str) -> None:
        """Show info message"""
        st.info(message)
    
    def validate_and_sanitize_input(self, text: str, field_name: str = "input") -> tuple[bool, str, str]:
        """
        Validate and sanitize user input
        Returns (is_valid, sanitized_text, error_message)
        """
        # Security check
        is_safe, security_reason = self.security_validator.is_safe_content(text)
        if not is_safe:
            return False, "", f"Invalid {field_name}: {security_reason}"
        
        # Sanitize input
        sanitized_text = self.validator.sanitize_input(text)
        
        return True, sanitized_text, ""
    
    def create_card(self, content: str, title: str = None, card_class: str = "default-card") -> None:
        """Create a styled card component"""
        card_html = f"""
        <div class="{card_class}">
            {f'<h3>{title}</h3>' if title else ''}
            {content}
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    def create_badge(self, text: str, badge_type: str = "primary") -> str:
        """Create a styled badge"""
        return f'<span class="badge badge-{badge_type}">{text}</span>'
    
    def create_metric_card(self, title: str, value: str, delta: str = None) -> None:
        """Create a metric card with optional delta"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if delta:
                st.metric(title, value, delta)
            else:
                st.metric(title, value)
    
    def handle_error(self, error: Exception, context: str = "") -> None:
        """Handle errors gracefully"""
        error_message = f"An error occurred{' in ' + context if context else ''}"
        details = str(error) if st.session_state.get('debug_mode', False) else None
        self.show_error(error_message, details)
        
        # Log error for debugging
        if hasattr(st.session_state, 'error_log'):
            st.session_state.error_log.append({
                'error': str(error),
                'context': context,
                'timestamp': st.session_state.get('current_time', 'unknown')
            })
    
    def add_animation_class(self, class_name: str = "fade-in-up") -> str:
        """Add animation class if animations are enabled"""
        if st.session_state.get('user_preferences', {}).get('animations_enabled', True):
            return f' class="{class_name}"'
        return ''
    
    def create_collapsible_section(self, title: str, content_func, expanded: bool = False):
        """Create a collapsible section"""
        with st.expander(title, expanded=expanded):
            content_func()
    
    def create_tabs(self, tab_names: list, tab_contents: list) -> None:
        """Create tabs with content"""
        tabs = st.tabs(tab_names)
        for tab, content_func in zip(tabs, tab_contents):
            with tab:
                content_func()

class ResponsiveLayout:
    """Helper class for responsive layout management"""
    
    @staticmethod
    def get_columns_config(screen_size: str = "desktop") -> list:
        """Get column configuration based on screen size"""
        configs = {
            "mobile": [1],
            "tablet": [1, 1],
            "desktop": [1, 2, 1],
            "wide": [1, 3, 1]
        }
        return configs.get(screen_size, configs["desktop"])
    
    @staticmethod
    def create_responsive_columns(content_funcs: list, screen_size: str = "desktop"):
        """Create responsive columns with content"""
        col_config = ResponsiveLayout.get_columns_config(screen_size)
        
        if len(content_funcs) <= len(col_config):
            columns = st.columns(col_config[:len(content_funcs)])
            for col, content_func in zip(columns, content_funcs):
                with col:
                    content_func()
        else:
            # If more content than columns, stack them
            for content_func in content_funcs:
                content_func()
    
    @staticmethod
    def create_sidebar_layout(sidebar_content_func, main_content_func):
        """Create a sidebar layout"""
        with st.sidebar:
            sidebar_content_func()
        
        main_content_func()

class NotificationManager:
    """Manages notifications and toast messages"""
    
    def __init__(self):
        self.initialize_notifications()
    
    def initialize_notifications(self):
        """Initialize notification system"""
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
    
    def add_notification(self, message: str, type: str = "info", duration: int = 5):
        """Add a notification"""
        notification = {
            'message': message,
            'type': type,
            'timestamp': st.session_state.get('current_time', 'now'),
            'duration': duration,
            'shown': False
        }
        st.session_state.notifications.append(notification)
    
    def show_notifications(self):
        """Display pending notifications"""
        if not st.session_state.notifications:
            return
        
        for i, notification in enumerate(st.session_state.notifications):
            if not notification['shown']:
                if notification['type'] == 'success':
                    st.success(notification['message'])
                elif notification['type'] == 'error':
                    st.error(notification['message'])
                elif notification['type'] == 'warning':
                    st.warning(notification['message'])
                else:
                    st.info(notification['message'])
                
                st.session_state.notifications[i]['shown'] = True
        
        # Clean up shown notifications
        st.session_state.notifications = [
            n for n in st.session_state.notifications if not n['shown']
        ]
    
    def clear_notifications(self):
        """Clear all notifications"""
        st.session_state.notifications = []