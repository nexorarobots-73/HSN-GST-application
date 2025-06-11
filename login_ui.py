from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QMessageBox, QWidget, QStackedWidget)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from login import OneDriveAuth

class LoginDialog(QDialog):
    loginSuccessful = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("HSN Tax Calculator - Login")
        self.setFixedSize(400, 300)
        self.auth = OneDriveAuth()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("HSN Tax Calculator")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Sign in with your Microsoft account")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Spacer
        layout.addSpacing(20)
        
        # Login button
        self.login_btn = QPushButton("Sign in with Microsoft")
        self.login_btn.setFixedHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)
        
        # Register button
        self.register_btn = QPushButton("Register with Microsoft")
        self.register_btn.setFixedHeight(40)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b6a0b;
            }
        """)
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)
        
        # Skip login button
        self.skip_btn = QPushButton("Continue without signing in")
        self.skip_btn.setStyleSheet("""
            QPushButton {
                color: #0078d4;
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.skip_btn.clicked.connect(self.skip_login)
        layout.addWidget(self.skip_btn)
        
        # Check if already logged in
        if self.auth.is_authenticated():
            token = self.auth.get_token_silent()
            if token:
                self.loginSuccessful.emit(token)
                self.accept()
        
        self.setLayout(layout)
    
    def login(self):
        try:
            result = self.auth.login()
            if "access_token" in result:
                self.loginSuccessful.emit(result)
                QMessageBox.information(self, "Success", "You have successfully signed in!")
                self.accept()
            else:
                QMessageBox.warning(self, "Login Failed", "Failed to sign in. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def register(self):
        # For Microsoft accounts, registration and login use the same flow
        self.login()
    
    def skip_login(self):
        reply = QMessageBox.question(self, "Continue without signing in", 
                                    "You won't be able to save data to OneDrive. Continue?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.accept()