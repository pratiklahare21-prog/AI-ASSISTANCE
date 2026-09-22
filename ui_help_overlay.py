"""
Help Overlay Widget for MARK LII
Displays keyboard shortcuts, tips, and quick start guide
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTabWidget, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QKeySequence, QShortcut

class HelpOverlay(QFrame):
    """
    Help overlay with tabs for shortcuts, tips, and guide
    """
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(700, 600)
        
        self._build_ui()
        
        # ESC to close
        QShortcut(QKeySequence("Esc"), self, self.close)
    
    def _build_ui(self):
        """Build the help overlay UI"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Container with rounded corners and background
        container = QFrame()
        container.setObjectName("helpContainer")
        container.setStyleSheet("""
            #helpContainer {
                background: #010d14;
                border: 2px solid #0d3347;
                border-radius: 12px;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📚 Help & Information")
        title.setStyleSheet("""
            color: #00d4ff;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #ff3355;
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #ff5577;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        container_layout.addLayout(header_layout)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #0d3347;
                border-radius: 8px;
                background: #010f18;
            }
            QTabBar::tab {
                background: #010f18;
                color: #5ab8cc;
                padding: 10px 20px;
                border: 1px solid #0d3347;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #011520;
                color: #00d4ff;
                border-color: #1a5c7a;
            }
            QTabBar::tab:hover {
                background: #011520;
                color: #00d4ff;
            }
        """)
        
        # Shortcuts tab
        shortcuts_widget = self._create_shortcuts_tab()
        tabs.addTab(shortcuts_widget, "⌨️ Shortcuts")
        
        # Quick Start tab
        quickstart_widget = self._create_quickstart_tab()
        tabs.addTab(quickstart_widget, "🚀 Quick Start")
        
        # Tips tab
        tips_widget = self._create_tips_tab()
        tabs.addTab(tips_widget, "💡 Tips & Tricks")
        
        # About tab
        about_widget = self._create_about_tab()
        tabs.addTab(about_widget, "ℹ️ About")
        
        container_layout.addWidget(tabs)
        
        # Footer
        footer = QLabel("Press ESC or click ✕ to close")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #3a8a9a; font-size: 11px;")
        container_layout.addWidget(footer)
        
        layout.addWidget(container)
    
    def _create_shortcuts_tab(self) -> QWidget:
        """Create keyboard shortcuts tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
            QTextEdit {
                background: #010d14;
                color: #8ffcff;
                border: 1px solid #0d3347;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }
        """)
        
        shortcuts = [
            ("Ctrl+M", "Mute/Unmute microphone"),
            ("Ctrl+,", "Open customization settings"),
            ("Ctrl+A", "Audio device settings"),
            ("Ctrl+K", "Memory panel"),
            ("Ctrl+P", "Plugin manager"),
            ("Ctrl+R", "Remote dashboard"),
            ("Ctrl+D", "Toggle quick drawer"),
            ("Ctrl+Q", "Quit application"),
            ("", ""),
            ("F11", "Toggle fullscreen"),
            ("F1", "Show this help"),
            ("Esc", "Interrupt/Close/Cancel"),
            ("Enter", "Send text command"),
            ("", ""),
            ("Ctrl+Plus", "Zoom in (if applicable)"),
            ("Ctrl+Minus", "Zoom out (if applicable)"),
            ("Ctrl+0", "Reset zoom (if applicable)"),
        ]
        
        content = "⌨️  KEYBOARD SHORTCUTS\n" + "=" * 50 + "\n\n"
        for shortcut, description in shortcuts:
            if shortcut:
                content += f"{shortcut:<20} {description}\n"
            else:
                content += "\n"
        
        text.setPlainText(content)
        layout.addWidget(text)
        
        return widget
    
    def _create_quickstart_tab(self) -> QWidget:
        """Create quick start guide tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
            QTextEdit {
                background: #010d14;
                color: #8ffcff;
                border: 1px solid #0d3347;
                border-radius: 6px;
                padding: 15px;
                font-size: 13px;
                line-height: 1.6;
            }
        """)
        
        content = """
🚀 QUICK START GUIDE
========================================

1️⃣  Setup Audio Devices
   • Click 🎧 button or press Ctrl+A
   • Select your microphone and speakers
   • Speak to test - watch the waveform react

2️⃣  Try Voice Commands
   • "What's the weather in New York?"
   • "Open Chrome"
   • "What's on my screen?"
   • "Set a reminder for 3 PM tomorrow"
   • "Play music on YouTube"
   • "Show my system status"

3️⃣  Use Text Input
   • Type commands in the input box below
   • Press Enter to send
   • Useful for precise commands or when voice isn't ideal

4️⃣  Process Files
   • Drag files onto the drop zone
   • Or click to browse files
   • Supports: Images, PDFs, Documents, Audio, Video, Code
   • Ask questions about uploaded files

5️⃣  Customize Assistant
   • Press Ctrl+, for customization
   • Change assistant name (default: JARVIS)
   • Pick a voice (Charon, Puck, Kore, Fenrir, Aoede)
   • Choose UI color theme

6️⃣  Manage Memory
   • Press Ctrl+K to view stored memories
   • JARVIS remembers your preferences
   • Delete any memory you don't want kept

7️⃣  Enable Plugins
   • Press Ctrl+P for plugin manager
   • Enable/disable features as needed
   • Create custom plugins (see docs)

8️⃣  Remote Control
   • Press Ctrl+R for QR code
   • Scan with phone to control remotely
   • Send commands from anywhere

📖 For detailed documentation:
   • README.md in project folder
   • docs/INSTALLATION.md for setup help
   • docs/TROUBLESHOOTING.md for issues

🎥 Video tutorials:
   • YouTube: @FatihMakes
   • https://www.youtube.com/@FatihMakes
""".strip()
        
        text.setPlainText(content)
        layout.addWidget(text)
        
        return widget
    
    def _create_tips_tab(self) -> QWidget:
        """Create tips and tricks tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
            QTextEdit {
                background: #010d14;
                color: #8ffcff;
                border: 1px solid #0d3347;
                border-radius: 6px;
                padding: 15px;
                font-size: 13px;
            }
        """)
        
        content = """
💡 TIPS & TRICKS
========================================

⚡ Performance
   • Close unused applications for better CPU
   • Use text input for faster responses
   • Disable visual effects if experiencing lag

🎤 Better Voice Recognition
   • Speak clearly and at normal pace
   • Reduce background noise
   • Use a quality microphone
   • Position mic 6-12 inches from mouth

🎯 Effective Commands
   • Be specific: "Open Chrome" not "open browser"
   • Ask follow-up questions naturally
   • Use screen capture: "What's on my screen?"
   • Reference files: "Summarize this PDF"

🧠 Memory Features
   • Say "Remember that..." for new facts
   • Ask "What did we discuss yesterday?"
   • Check memory panel to see stored info
   • Delete outdated memories regularly

📁 File Processing
   • Drag multiple files at once
   • Ask specific questions about files
   • Use for code review, document analysis
   • Convert between formats

⚙️ Customization
   • Try different voices for personality
   • Match UI color to your setup
   • Enable morning briefing for daily summary
   • Set auto-start for convenience

🔌 Plugins
   • Check plugin manager for new features
   • Disable unused plugins to save resources
   • Create custom plugins (see CONTRIBUTING.md)

🌐 Browser Control
   • "Open YouTube in Chrome"
   • "Search for AI news"
   • Automate web tasks
   • Take screenshots of pages

⏰ Reminders & Automation
   • Set reminders with natural language
   • Schedule system tasks
   • Monitor topics for updates
   • Track game updates (Steam/Epic)

🔒 Privacy
   • All data stored locally
   • Memory in memory/long_term.json
   • Delete any stored information anytime
   • No data sent except to Gemini API

🆘 Troubleshooting
   • Restart if unresponsive
   • Check docs/TROUBLESHOOTING.md
   • Verify API key in config
   • Run check_requirements.py

🎓 Learning Resources
   • YouTube: @FatihMakes
   • GitHub: Star the repo for updates
   • docs/ folder for detailed guides
""".strip()
        
        text.setPlainText(content)
        layout.addWidget(text)
        
        return widget
    
    def _create_about_tab(self) -> QWidget:
        """Create about tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Title
        title = QLabel("⚙️ MARK LII")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #00d4ff;
            font-size: 32px;
            font-weight: bold;
            margin: 20px 0;
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("AI Personal Assistant")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            color: #5ab8cc;
            font-size: 16px;
            margin-bottom: 20px;
        """)
        layout.addWidget(subtitle)
        
        # Info text
        info = QTextEdit()
        info.setReadOnly(True)
        info.setMaximumHeight(300)
        info.setStyleSheet("""
            QTextEdit {
                background: #010d14;
                color: #8ffcff;
                border: 1px solid #0d3347;
                border-radius: 6px;
                padding: 15px;
                font-size: 13px;
            }
        """)
        
        info_text = """
A real-time voice AI assistant that can hear, see, 
understand, and control your computer.

Built with:
• Google Gemini Live API
• PyQt6 for modern UI
• Native audio streaming
• Cross-platform support

Features:
• Real-time voice conversation
• Visual awareness (screen & camera)
• System control & automation
• Persistent memory
• Plugin architecture
• Remote access via QR code

Created by: FatihMakes
License: CC BY-NC 4.0
Platform: Windows, macOS, Linux
Python: 3.11 - 3.12

Links:
• YouTube: @FatihMakes
• Instagram: @fatihmakes
• GitHub: FatihMakes/Mark-LII

Version: Mark LII (52)
""".strip()
        
        info.setPlainText(info_text)
        layout.addWidget(info)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel("Made with ❤️ by the community")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #3a8a9a; font-size: 11px; margin-top: 10px;")
        layout.addWidget(footer)
        
        return widget
    
    def closeEvent(self, event):
        """Override close event to emit signal"""
        self.closed.emit()
        super().closeEvent(event)
