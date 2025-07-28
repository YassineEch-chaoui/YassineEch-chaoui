"""
Contact section component with form validation
"""
import streamlit as st
import time
from components.base import BaseComponent, ResponsiveLayout
from config.constants import CONTACT_INFO, SUCCESS_MESSAGES, ERROR_MESSAGES, LOADING_MESSAGES
from utils.validators import InputValidator

class ContactSection(BaseComponent):
    """Renders the Contact section with form"""
    
    def __init__(self, theme_manager=None):
        super().__init__(theme_manager)
    
    def render(self) -> None:
        """Render the contact section"""
        try:
            self._render_section_header()
            self._render_contact_content()
        except Exception as e:
            self.handle_error(e, "contact section rendering")
    
    def _render_section_header(self) -> None:
        """Render section header"""
        st.markdown('<h2 class="section-header">📬 Get In Touch</h2>', unsafe_allow_html=True)
    
    def _render_contact_content(self) -> None:
        """Render main contact content"""
        # Use responsive layout
        def render_contact_info():
            self._render_contact_information()
        
        def render_contact_form():
            self._render_contact_form()
        
        # Check if compact mode is enabled
        compact_mode = st.session_state.get('user_preferences', {}).get('compact_mode', False)
        
        if compact_mode:
            render_contact_info()
            render_contact_form()
        else:
            ResponsiveLayout.create_responsive_columns([
                render_contact_info,
                render_contact_form
            ], "desktop")
    
    def _render_contact_information(self) -> None:
        """Render contact information section"""
        contact_html = f"""
        <div class="contact-info"{self.add_animation_class()}>
            <h3>📧 Contact Information</h3>
            <p>{CONTACT_INFO['description']}</p>
            
            <div class="contact-links">
                <div class="contact-link">
                    <strong>🐙 GitHub:</strong> 
                    <a href="{CONTACT_INFO['github_url']}" target="_blank">
                        YassineEch-chaoui
                    </a>
                </div>
                
                <div class="contact-link">
                    <strong>💼 Professional Networks:</strong> 
                    <span>Feel free to connect with me on professional platforms</span>
                </div>
                
                <div class="contact-link">
                    <strong>📩 Email:</strong> 
                    <span>Available upon request</span>
                </div>
                
                <div class="contact-link">
                    <strong>🌍 Location:</strong> 
                    <span>Available for remote opportunities</span>
                </div>
            </div>
            
            {self._render_social_links()}
            
            {self._render_availability_status()}
        </div>
        """
        st.markdown(contact_html, unsafe_allow_html=True)
    
    def _render_social_links(self) -> str:
        """Render social media links"""
        return """
        <div class="social-links">
            <h4>🔗 Connect With Me</h4>
            <div class="social-buttons">
                <a href="https://github.com/YassineEch-chaoui" target="_blank" class="social-btn github">
                    GitHub
                </a>
                <a href="#" class="social-btn linkedin" onclick="return false;">
                    LinkedIn
                </a>
                <a href="#" class="social-btn twitter" onclick="return false;">
                    Twitter
                </a>
                <a href="#" class="social-btn discord" onclick="return false;">
                    Discord
                </a>
            </div>
        </div>
        """
    
    def _render_availability_status(self) -> str:
        """Render current availability status"""
        return """
        <div class="availability-status">
            <h4>📅 Availability</h4>
            <div class="status-indicator">
                <span class="status-dot available"></span>
                <span class="status-text">Available for new opportunities</span>
            </div>
            <div class="status-details">
                <small>• Open to full-time positions</small><br>
                <small>• Available for freelance projects</small><br>
                <small>• Interested in collaboration</small>
            </div>
        </div>
        """
    
    def _render_contact_form(self) -> None:
        """Render contact form with validation"""
        st.markdown("### 💌 Send me a message")
        
        # Initialize form state
        if 'form_submitted' not in st.session_state:
            st.session_state.form_submitted = False
        
        if 'form_errors' not in st.session_state:
            st.session_state.form_errors = {}
        
        with st.form("contact_form", clear_on_submit=False):
            # Form fields
            name = st.text_input(
                "Your Name *", 
                placeholder="Enter your full name",
                help="Please provide your full name"
            )
            
            email = st.text_input(
                "Your Email *", 
                placeholder="your.email@example.com",
                help="We'll use this to respond to your message"
            )
            
            subject = st.text_input(
                "Subject *", 
                placeholder="Brief description of your message",
                help="What is this message about?"
            )
            
            message = st.text_area(
                "Message *", 
                height=120,
                placeholder="Tell me about your project, question, or how we can work together...",
                help="Please provide details about your inquiry"
            )
            
            # Form options
            col1, col2 = st.columns(2)
            
            with col1:
                urgent = st.checkbox("🔥 Urgent", help="Mark as urgent priority")
            
            with col2:
                copy_self = st.checkbox("📧 Send me a copy", help="Send a copy to your email")
            
            # Submit button
            submitted = st.form_submit_button(
                "📤 Send Message",
                type="primary",
                use_container_width=True
            )
            
            # Handle form submission
            if submitted:
                self._handle_form_submission(name, email, subject, message, urgent, copy_self)
        
        # Display form status
        self._display_form_status()
    
    def _handle_form_submission(self, name: str, email: str, subject: str, message: str, urgent: bool, copy_self: bool) -> None:
        """Handle contact form submission with validation"""
        try:
            # Clear previous errors
            st.session_state.form_errors = {}
            
            # Validate form data
            errors = self.validator.validate_contact_form(name, email, subject, message)
            
            if errors:
                st.session_state.form_errors = errors
                st.session_state.form_submitted = False
                return
            
            # Sanitize form data
            sanitized_data = self.validator.sanitize_contact_form(name, email, subject, message)
            
            # Security check
            for field, value in sanitized_data.items():
                is_safe, _, security_error = self.validate_and_sanitize_input(value, field)
                if not is_safe:
                    st.session_state.form_errors[field] = security_error
                    st.session_state.form_submitted = False
                    return
            
            # Simulate sending message
            self._simulate_message_sending(sanitized_data, urgent, copy_self)
            
        except Exception as e:
            self.handle_error(e, "form submission")
            st.session_state.form_errors['general'] = "An error occurred while sending your message."
    
    def _simulate_message_sending(self, data: dict, urgent: bool, copy_self: bool) -> None:
        """Simulate message sending process"""
        with st.spinner(LOADING_MESSAGES['sending_message']):
            # Simulate processing time
            time.sleep(2)
            
            # Log the message (in a real app, this would send an email or save to database)
            self._log_contact_message(data, urgent, copy_self)
            
            # Mark as successfully submitted
            st.session_state.form_submitted = True
            st.session_state.form_errors = {}
            
            # Track successful form submission
            self._track_form_submission()
    
    def _log_contact_message(self, data: dict, urgent: bool, copy_self: bool) -> None:
        """Log contact message (placeholder for real implementation)"""
        # In a real application, this would:
        # 1. Send email notification
        # 2. Save to database
        # 3. Send auto-reply
        # 4. Notify administrators
        
        message_log = {
            'timestamp': time.time(),
            'name': data['name'],
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message'][:100] + '...',  # Truncate for logging
            'urgent': urgent,
            'copy_requested': copy_self,
            'ip_address': 'hidden',  # Would capture real IP in production
            'user_agent': 'hidden'   # Would capture real user agent in production
        }
        
        # Store in session state for demo purposes
        if 'contact_messages' not in st.session_state:
            st.session_state.contact_messages = []
        
        st.session_state.contact_messages.append(message_log)
    
    def _track_form_submission(self) -> None:
        """Track form submission for analytics"""
        if 'form_submissions' not in st.session_state:
            st.session_state.form_submissions = 0
        
        st.session_state.form_submissions += 1
    
    def _display_form_status(self) -> None:
        """Display form submission status and errors"""
        # Show success message
        if st.session_state.get('form_submitted', False):
            st.success(SUCCESS_MESSAGES['message_sent'])
            
            # Reset form state after showing success
            if st.button("Send Another Message"):
                st.session_state.form_submitted = False
                st.rerun()
        
        # Show validation errors
        if st.session_state.get('form_errors', {}):
            for field, error in st.session_state.form_errors.items():
                if field == 'general':
                    st.error(error)
                else:
                    st.error(f"**{field.title()}:** {error}")
    
    def render_contact_stats(self) -> None:
        """Render contact form statistics (admin view)"""
        if st.session_state.get('debug_mode', False):
            with st.expander("📊 Contact Form Statistics", expanded=False):
                submissions = st.session_state.get('form_submissions', 0)
                messages = st.session_state.get('contact_messages', [])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total Submissions", submissions)
                
                with col2:
                    st.metric("Messages Logged", len(messages))
                
                if messages:
                    st.markdown("#### Recent Messages")
                    for msg in messages[-5:]:  # Show last 5 messages
                        st.write(f"**{msg['name']}** - {msg['subject']}")
                        st.caption(f"Sent at: {time.ctime(msg['timestamp'])}")
    
    def render_faq_section(self) -> None:
        """Render FAQ section"""
        with st.expander("❓ Frequently Asked Questions", expanded=False):
            faqs = [
                {
                    "question": "How quickly do you respond to messages?",
                    "answer": "I typically respond within 24-48 hours during business days."
                },
                {
                    "question": "What type of projects are you interested in?",
                    "answer": "I'm interested in web development, data analysis, automation, and innovative tech projects."
                },
                {
                    "question": "Do you offer freelance services?",
                    "answer": "Yes, I'm available for freelance projects. Please include project details in your message."
                },
                {
                    "question": "Are you open to remote work?",
                    "answer": "Absolutely! I'm experienced with remote collaboration and various communication tools."
                }
            ]
            
            for faq in faqs:
                st.markdown(f"**Q: {faq['question']}**")
                st.markdown(f"A: {faq['answer']}")
                st.markdown("---")
    
    def get_contact_css(self) -> str:
        """Get additional CSS for contact section"""
        return """
        <style>
        .contact-links {
            margin: 1.5rem 0;
        }
        
        .contact-link {
            margin: 1rem 0;
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border-color);
        }
        
        .contact-link:last-child {
            border-bottom: none;
        }
        
        .contact-link strong {
            color: var(--primary-color);
        }
        
        .contact-link a {
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: 500;
        }
        
        .contact-link a:hover {
            color: var(--primary-color);
        }
        
        .social-links {
            margin: 2rem 0;
        }
        
        .social-links h4 {
            color: var(--secondary-color);
            margin-bottom: 1rem;
        }
        
        .social-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .social-btn {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.8rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .social-btn.github {
            background: #333;
            color: white;
        }
        
        .social-btn.linkedin {
            background: #0077b5;
            color: white;
        }
        
        .social-btn.twitter {
            background: #1da1f2;
            color: white;
        }
        
        .social-btn.discord {
            background: #7289da;
            color: white;
        }
        
        .social-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        .availability-status {
            margin: 2rem 0;
            padding: 1rem;
            background: var(--surface-color);
            border-radius: 10px;
            border-left: 4px solid #28a745;
        }
        
        .availability-status h4 {
            color: var(--text-primary);
            margin-bottom: 1rem;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .status-dot.available {
            background: #28a745;
        }
        
        .status-dot.busy {
            background: #ffc107;
        }
        
        .status-dot.unavailable {
            background: #dc3545;
        }
        
        .status-text {
            font-weight: 500;
            color: var(--text-primary);
        }
        
        .status-details {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(40, 167, 69, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(40, 167, 69, 0);
            }
        }
        
        /* Form styling enhancements */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: var(--surface-color);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
            outline: none;
        }
        
        .stCheckbox > label {
            color: var(--text-primary);
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .social-buttons {
                justify-content: center;
            }
            
            .availability-status {
                padding: 0.8rem;
            }
        }
        </style>
        """