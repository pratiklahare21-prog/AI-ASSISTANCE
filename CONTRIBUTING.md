# 🤝 Contributing to MARK LII

Thank you for your interest in contributing to MARK LII! While this is primarily a personal project by FatihMakes, we welcome bug reports, feature suggestions, and community feedback.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Plugin Development](#plugin-development)
- [Testing](#testing)
- [Documentation](#documentation)

---

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Help us fix it!

1. **Check Existing Issues:** Search [GitHub Issues](https://github.com/FatihMakes/Mark-LII/issues) to see if it's already reported
2. **Create Detailed Bug Report:** Include:
   - **OS and Version:** Windows 11, macOS 14, Ubuntu 22.04, etc.
   - **Python Version:** Run `python --version`
   - **Steps to Reproduce:** Clear, numbered steps
   - **Expected Behavior:** What should happen
   - **Actual Behavior:** What actually happens
   - **Error Messages:** Full error output
   - **Screenshots:** If applicable

### 💡 Suggesting Features

Have an idea to improve MARK LII?

1. **Check Existing Suggestions:** See if someone already proposed it
2. **Open Feature Request:** Use the "Feature Request" template
3. **Describe the Feature:**
   - What problem does it solve?
   - How would it work?
   - Why is it valuable?
   - Any implementation ideas?

### 🔧 Code Contributions

**Note:** Direct code contributions require discussion first.

1. **Open an Issue First:** Discuss your idea before writing code
2. **Wait for Approval:** Ensure the maintainer is interested
3. **Fork the Repository**
4. **Create Feature Branch:** `git checkout -b feature/your-feature-name`
5. **Make Your Changes**
6. **Test Thoroughly**
7. **Submit Pull Request**

---

## Development Setup

### Prerequisites

- Python 3.11 or 3.12
- Git
- Text editor or IDE (VS Code recommended)

### Setup Steps

```bash
# 1. Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/Mark-LII.git
cd Mark-LII

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development tools
pip install black flake8 mypy pytest

# 5. Configure API key
cp config/api_keys.json.example config/api_keys.json
# Edit api_keys.json with your Gemini API key

# 6. Run the project
python main.py
```

---

## Code Style Guidelines

### Python Style

MARK LII follows PEP 8 with some modifications:

- **Line Length:** 88 characters (Black default)
- **Quotes:** Double quotes for strings
- **Imports:** Grouped by stdlib, third-party, local
- **Type Hints:** Encouraged but not required
- **Docstrings:** Google-style docstrings

### Formatting

Use **Black** for automatic formatting:

```bash
# Format all Python files
black .

# Check formatting without changes
black --check .
```

### Linting

Use **flake8** to catch common issues:

```bash
flake8 actions/ core/ memory/
```

### Type Checking (Optional)

```bash
mypy main.py
```

---

## Plugin Development

The easiest way to contribute is by creating plugins!

### Plugin Template

Copy `plugins/_template.py` and follow this structure:

```python
"""
Plugin Name: My Awesome Plugin
Description: Brief description of what it does
Author: Your Name
Version: 1.0.0
"""

PLUGIN_INFO = {
    "name": "my_plugin",
    "description": "Does something awesome",
    "version": "1.0.0",
    "author": "Your Name",
    "enabled": True,
}

TOOL_DECLARATION = {
    "name": "my_plugin_action",
    "description": "Clear description for the AI model",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "param_name": {
                "type": "STRING",
                "description": "Parameter description"
            }
        },
        "required": ["param_name"]
    }
}

def execute(params: dict) -> str:
    """
    Main execution function called by MARK LII
    
    Args:
        params: Dictionary of parameters from AI model
        
    Returns:
        Result string to be read by the AI
    """
    # Your implementation here
    result = f"Processed: {params.get('param_name')}"
    return result
```

### Plugin Guidelines

- **Single File:** Keep each plugin in one `.py` file
- **No Side Effects:** Don't modify global state
- **Error Handling:** Use try/except, never crash
- **Clear Descriptions:** Help the AI understand when to use your plugin
- **Return Strings:** Always return a result message
- **Dependencies:** Document any extra pip packages needed

### Testing Your Plugin

1. Place in `plugins/` directory
2. Restart MARK LII
3. Check plugin appears in plugin manager
4. Test with voice commands

---

## Testing

### Manual Testing

Before submitting changes:

1. **Run MARK LII:** Ensure it starts without errors
2. **Test Core Features:**
   - Voice input/output
   - System control commands
   - File operations
   - Memory persistence
3. **Test Your Changes:** Specific functionality you modified
4. **Test on Different OS:** If possible, test Windows/macOS/Linux

### Automated Testing (Coming Soon)

```bash
# Run test suite
pytest tests/

# With coverage
pytest --cov=actions --cov=core --cov=memory tests/
```

---

## Documentation

### Updating Documentation

When making changes, update relevant docs:

- **README.md:** For major features or installation changes
- **docs/INSTALLATION.md:** For setup process changes
- **docs/TROUBLESHOOTING.md:** Add common issues you discover
- **Code Comments:** Explain complex logic
- **Docstrings:** Document functions and classes

### Writing Good Documentation

- **Be Clear:** Assume reader is new to the project
- **Use Examples:** Show, don't just tell
- **Keep Updated:** Remove outdated information
- **Test Instructions:** Verify steps actually work

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines (run `black` and `flake8`)
- [ ] Tested on your system
- [ ] Updated relevant documentation
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test this?

## Screenshots (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No warnings or errors
```

---

## Questions?

- **GitHub Issues:** For bug reports and feature requests
- **Discussions:** For general questions
- **YouTube:** [@FatihMakes](https://www.youtube.com/@FatihMakes) for video tutorials

---

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for helping make MARK LII better! 🚀
