# 💻 Yassine Ech-chaoui - Portfolio

> **Modern, Responsive Streamlit Portfolio Application**

A sophisticated portfolio web application built with Streamlit, featuring modular architecture, adaptive theming, and comprehensive functionality.

![Portfolio Demo](https://github.com/user-attachments/assets/0bc2004d-dec3-4810-aaae-3fc4ee745489)

## 🚀 Features

### 🎨 **Modern UI & Theming**
- **Adaptive Dark/Light Mode**: Automatically detects system theme preference
- **Manual Theme Toggle**: Users can switch between light, dark, and auto modes
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern CSS**: Clean, professional styling with smooth animations
- **Google Fonts Integration**: Enhanced typography with Inter font family

### 🏗️ **Modular Architecture**
- **Component-Based Design**: Separate, reusable components for each section
- **Class-Based Structure**: Object-oriented approach for better maintainability
- **Configuration Management**: Centralized constants and settings
- **Error Handling**: Comprehensive error handling throughout the application

### 🔧 **Performance & Optimization**
- **Intelligent Caching**: API responses cached with configurable TTL
- **Performance Monitoring**: Built-in performance tracking and metrics
- **Lazy Loading**: Components load only when needed
- **Memory Management**: Optimized handling of large data sets

### 🛡️ **Security & Validation**
- **Input Validation**: Comprehensive form validation and sanitization
- **XSS Protection**: Built-in security against cross-site scripting
- **Environment Variables**: Sensitive data stored in environment variables
- **Safe URL Validation**: All external links validated for security

### 📱 **Interactive Features**
- **GitHub Integration**: Real-time repository and statistics fetching
- **Contact Form**: Validated contact form with comprehensive error handling
- **User Preferences**: Customizable settings stored in session state
- **Progress Tracking**: Visit counter and usage analytics

## 🏛️ Architecture

```
📁 Portfolio Application
├── 📄 app.py                 # Main application entry point
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env.example          # Environment variables template
├── 📁 config/               # Configuration management
│   ├── 📄 constants.py      # Application constants
│   ├── 📄 settings.py       # Settings and session management
│   └── 📄 __init__.py
├── 📁 components/           # UI Components
│   ├── 📄 base.py           # Base component class
│   ├── 📄 header.py         # Header component
│   ├── 📄 sidebar.py        # Sidebar navigation
│   ├── 📁 sections/         # Page sections
│   │   ├── 📄 about.py      # About Me section
│   │   ├── 📄 skills.py     # Skills & Technologies
│   │   ├── 📄 projects.py   # Projects showcase
│   │   ├── 📄 github_stats.py # GitHub statistics
│   │   ├── 📄 contact.py    # Contact form
│   │   └── 📄 __init__.py
│   └── 📄 __init__.py
├── 📁 utils/                # Utility modules
│   ├── 📄 theme_manager.py  # Theme and CSS management
│   ├── 📄 validators.py     # Input validation utilities
│   ├── 📄 cache_manager.py  # Caching and performance
│   └── 📄 __init__.py
└── 📁 assets/               # Static assets
    └── 📁 styles/
        └── 📄 main.css      # Main stylesheet
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YassineEch-chaoui/YassineEch-chaoui.git
   cd YassineEch-chaoui
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# GitHub Integration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_USERNAME=YassineEch-chaoui

# Email Service (for contact form)
EMAIL_SERVICE_KEY=your_email_service_api_key
EMAIL_FROM=noreply@yourdomain.com
EMAIL_TO=your_email@yourdomain.com

# Application Settings
STREAMLIT_ENV=production
DEBUG_MODE=false

# Performance
CACHE_TTL=3600
```

### Customization

**Personal Information**: Edit `config/constants.py` to update:
- Developer name and tagline
- Skills and technologies
- Contact information
- About me content

**Styling**: Modify `utils/theme_manager.py` and `assets/styles/main.css` to:
- Change color schemes
- Adjust typography
- Modify component styling
- Add new animations

**Features**: Enable/disable features in `config/constants.py`:
- Contact form
- GitHub integration
- Analytics tracking
- Theme switching

## 📱 Usage

### Navigation
- Use the sidebar to navigate between sections
- Toggle theme using the theme selector
- Adjust preferences in the sidebar settings

### Sections
1. **About Me**: Personal introduction and background
2. **Skills & Technologies**: Technical skills with proficiency levels
3. **Projects**: GitHub repositories showcase with filtering
4. **GitHub Stats**: Real-time GitHub statistics and activity
5. **Contact**: Contact form with validation and social links

### Theme System
- **Auto**: Follows system preference (default)
- **Light**: Force light theme
- **Dark**: Force dark theme

## 🔧 Development

### Adding New Sections

1. Create a new component in `components/sections/`
2. Extend the `BaseComponent` class
3. Add the section to navigation in `config/constants.py`
4. Import and initialize in `app.py`

### Customizing Themes

1. Edit CSS variables in `utils/theme_manager.py`
2. Add new color schemes in `config/constants.py`
3. Update component styling as needed

### Performance Optimization

- Use `@cached_function` decorator for expensive operations
- Monitor performance with built-in performance tracking
- Adjust cache TTL in configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact

- **GitHub**: [@YassineEch-chaoui](https://github.com/YassineEch-chaoui)
- **Email**: Available through the contact form in the application

---

## 💫 About Me:

I turn ideas into apps and caffeine into code ☕💡<br>
Powered by memes and deadlines 😅🔥<br>
Collecting knowledge like it's Pokémon 🧠🎒<br>
Turning curiosity into creation 💡🛠️<br>
Gym rat with a GitHub account 💪📂<br>
Coding like Thorfinn fights: with patience, purpose, and rage 🔥🗡️

## 💻 Tech Stack:
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=flat&logo=javascript&logoColor=%23F7DF1E) ![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=flat&logo=typescript&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=flat&logo=css3&logoColor=white) ![C#](https://img.shields.io/badge/c%23-%23239120.svg?style=flat&logo=csharp&logoColor=white) ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=flat&logo=c%2B%2B&logoColor=white) ![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=flat&logo=openjdk&logoColor=white) ![Kotlin](https://img.shields.io/badge/kotlin-%237F52FF.svg?style=flat&logo=kotlin&logoColor=white) ![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=flat&logo=powershell&logoColor=white) ![Bash Script](https://img.shields.io/badge/bash_script-%23121011.svg?style=flat&logo=gnu-bash&logoColor=white) ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=flat&logo=microsoftazure&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=flat&logo=git&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=flat&logo=django&logoColor=white) ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=flat&logo=mysql&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=flat&logo=mongodb&logoColor=white)

## 📊 GitHub Stats:

![](https://github-readme-stats.vercel.app/api/top-langs/?username=YassineEch-chaoui&theme=bear&hide_border=false&include_all_commits=false&count_private=false&layout=compact)

---
[![](https://visitcount.itsvg.in/api?id=YassineEch-chaoui&icon=0&color=0)](https://visitcount.itsvg.in)