from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from msal import PublicClientApplication
import json, os
from dotenv import load_dotenv
from crypto_utils import encrypt_pin, decrypt_pin
import keyring

# Load environment variables
load_dotenv()

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str, str)  # Signal to emit when login is successful (email, name)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - HSN Tax App")
        self.resize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()

        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setPlaceholderText("Enter 4-digit PIN")

        # Buttons
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        
        self.forgot_btn = QPushButton("Forgot PIN")
        self.forgot_btn.setStyleSheet("color: #2196F3;")

        # Microsoft login button
        self.ms_login_btn = QPushButton("Login with Microsoft")
        self.ms_login_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 8px;")

        # Add widgets to layout
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("PIN:"))
        layout.addWidget(self.pin_input)

        layout.addWidget(self.signup_btn)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.forgot_btn)
        layout.addWidget(QLabel("OR"))
        layout.addWidget(self.ms_login_btn)

        # Connect signals
        self.signup_btn.clicked.connect(self.signup)
        self.login_btn.clicked.connect(self.login)
        self.forgot_btn.clicked.connect(self.forgot_pin)
        self.ms_login_btn.clicked.connect(self.microsoft_login)

        self.setLayout(layout)

    def signup(self):
        name = self.name_input.text()
        email = self.email_input.text()
        pin = self.pin_input.text()

        if not all([name, email, pin]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
            
        if len(pin) != 4 or not pin.isdigit():
            QMessageBox.warning(self, "Error", "PIN must be 4 digits")
            return

        try:
            keyring.set_password("HSNAppService", f"{email}_name", name)
            keyring.set_password("HSNAppService", f"{email}_pin", encrypt_pin(pin))
            QMessageBox.information(self, "Success", "User registered successfully!")
            self.login_successful.emit(email, name)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")

    def login(self):
        email = self.email_input.text()
        pin = self.pin_input.text()
        
        if not email or not pin:
            QMessageBox.warning(self, "Error", "Please enter email and PIN")
            return
            
        try:
            name = keyring.get_password("HSNAppService", f"{email}_name")
            enc_pin = keyring.get_password("HSNAppService", f"{email}_pin")
            
            if not name or not enc_pin:
                QMessageBox.warning(self, "Error", "User not found")
                return
                
            if decrypt_pin(enc_pin) != pin:
                QMessageBox.warning(self, "Error", "Invalid PIN")
                return
                
            QMessageBox.information(self, "Success", f"Welcome back, {name}!")
            self.login_successful.emit(email, name)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

    def forgot_pin(self):
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Error", "Please enter your registered email")
            return
            
        try:
            name = keyring.get_password("HSNAppService", f"{email}_name")
            if not name:
                QMessageBox.warning(self, "Error", "Email not found")
                return
                
            keyring.delete_password("HSNAppService", f"{email}_pin")
            QMessageBox.information(self, "PIN Reset", "Your PIN has been reset. Please register again.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"PIN reset failed: {str(e)}")

    def microsoft_login(self):
        try:
            client_id = os.getenv("CLIENT_ID")
            authority = os.getenv("AUTHORITY")
            
            if not client_id or not authority:
                QMessageBox.warning(self, "Configuration Error", "Microsoft login is not configured properly")
                return
                
            app = PublicClientApplication(client_id=client_id, authority=authority)
            scopes = os.getenv("SCOPES", "User.Read").split()
            
            result = app.acquire_token_interactive(scopes=scopes)
            
            if "access_token" in result:
                # Get user info
                email = result.get("account", {}).get("username", "")
                name = email.split("@")[0]  # Simple name extraction
                
                QMessageBox.information(self, "Success", f"Microsoft login successful!\nWelcome, {name}")
                self.login_successful.emit(email, name)
                self.close()
            else:
                QMessageBox.warning(self, "Login Failed", "Microsoft login failed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Microsoft login error: {str(e)}")


# For testing the login window independently
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())