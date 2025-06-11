import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, 
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                             QMessageBox, QFileDialog, QDesktopWidget, QStatusBar)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from hsn_loader import load_hsn_codes
from tax_logic import calculate_tax
from storage import save_entry
from login import LoginWindow
from onedrive_sync import upload_to_onedrive, download_from_onedrive

class HSNApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HSN Tax Calculator")
        self.setGeometry(100, 100, 1080, 720)
        self.center_screen()
        
        # User info
        self.user_email = None
        self.user_name = None
        
        # Show login window first
        self.show_login()
        
        # Load HSN data
        self.hsn_codes, self.hsn_map = load_hsn_codes()
        
        # Initialize UI
        self.initUI()
        
    def show_login(self):
        """Show login window and handle login result"""
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
        
    def on_login_success(self, email, name):
        """Handle successful login"""
        self.user_email = email
        self.user_name = name
        self.statusBar().showMessage(f"Logged in as: {name} ({email})")
        
    def center_screen(self):
        """Center window on screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def initUI(self):
        """Initialize the main UI"""
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        if self.user_name:
            self.statusBar.showMessage(f"Logged in as: {self.user_name} ({self.user_email})")
        else:
            self.statusBar.showMessage("Not logged in")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # HSN Code dropdown
        self.hsn_label = QLabel("Select HSN Code:")
        self.hsn_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.hsn_label)
        
        self.hsn_combo = QComboBox()
        for code in self.hsn_codes:
            desc = self.hsn_map.get(code, '')
            self.hsn_combo.addItem(f"{code} - {desc}")
        self.hsn_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.hsn_combo)
        
        # Description
        self.desc_label = QLabel("Description:")
        self.desc_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.desc_label)
        
        self.desc_value = QLabel()
        self.desc_value.setStyleSheet("background-color: white; padding: 10px; border: 1px solid #ccc; font-size: 14px;")
        layout.addWidget(self.desc_value)
        
        # Quantity type
        self.qty_type_label = QLabel("Quantity Type:")
        self.qty_type_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.qty_type_label)
        
        self.qty_type_combo = QComboBox()
        self.qty_type_combo.addItems(["Units", "Kilograms", "Liters", "Meters", "Pieces"])
        self.qty_type_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.qty_type_combo)
        
        # Quantity
        self.qty_label = QLabel("Quantity:")
        self.qty_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.qty_label)
        
        self.qty_input = QLineEdit()
        self.qty_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.qty_input.setPlaceholderText("Enter quantity")
        layout.addWidget(self.qty_input)
        
        # Base value input
        self.value_label = QLabel("Enter Taxable Value (₹):")
        self.value_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.value_label)
        
        self.value_input = QLineEdit()
        self.value_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.value_input.setPlaceholderText("Enter taxable value")
        layout.addWidget(self.value_input)
        
        # Tax slab dropdown
        self.tax_label = QLabel("Select Tax Slab:")
        self.tax_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.tax_label)
        
        self.tax_combo = QComboBox()
        self.tax_combo.addItems(["0%", "0.25%", "3%", "5%", "12%", "18%", "28%"])
        self.tax_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.tax_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.calc_button = QPushButton("Calculate Tax")
        self.calc_button.setStyleSheet("padding: 10px; background-color: #4CAF50; color: white; font-size: 14px;")
        self.calc_button.clicked.connect(self.calculate_tax)
        button_layout.addWidget(self.calc_button)
        
        self.save_button = QPushButton("Save Entry")
        self.save_button.setStyleSheet("padding: 10px; background-color: #2196F3; color: white; font-size: 14px;")
        self.save_button.clicked.connect(self.save_entry)
        button_layout.addWidget(self.save_button)
        
        self.export_button = QPushButton("Export CSV")
        self.export_button.setStyleSheet("padding: 10px; background-color: #FF9800; color: white; font-size: 14px;")
        self.export_button.clicked.connect(self.export_csv)
        button_layout.addWidget(self.export_button)
        
        # OneDrive sync button
        self.sync_button = QPushButton("Sync to OneDrive")
        self.sync_button.setStyleSheet("padding: 10px; background-color: #0078d4; color: white; font-size: 14px;")
        self.sync_button.clicked.connect(self.sync_to_onedrive)
        button_layout.addWidget(self.sync_button)
        
        layout.addLayout(button_layout)
        
        # Result display
        self.result_label = QLabel("Tax calculation will appear here")
        self.result_label.setStyleSheet("background-color: white; padding: 15px; border: 1px solid #ccc; font-size: 14px;")
        layout.addWidget(self.result_label)
        
        central_widget.setLayout(layout)
        
        # Connect signals
        self.hsn_combo.currentIndexChanged.connect(self.update_description)
        
        # Initial update
        self.update_description()
        
    def update_description(self):
        hsn_code = self.hsn_combo.currentText().split(" - ")[0]
        desc = self.hsn_map.get(hsn_code, '')
        self.desc_value.setText(desc)
        
    def calculate_tax(self):
        try:
            value = float(self.value_input.text() or 0)
            qty = float(self.qty_input.text() or 1)
            tax_slab = self.tax_combo.currentText()
            hsn_code = self.hsn_combo.currentText().split(" - ")[0]
            qty_type = self.qty_type_combo.currentText()
            
            # Calculate tax
            cgst, sgst = calculate_tax(value, tax_slab)
            total_tax = cgst + sgst
            final_amount = value + total_tax
            
            # Store current calculation
            self.current_entry = {
                'HSN': hsn_code,
                'Description': self.hsn_map.get(hsn_code, ''),
                'QtyType': qty_type,
                'Qty': qty,
                'BaseValue': value,
                'TaxSlab': tax_slab,
                'CGST': cgst,
                'SGST': sgst,
                'TotalTax': total_tax,
                'FinalAmount': final_amount,
                'UserEmail': self.user_email or 'anonymous'
            }
            
            # Format result
            result = f"""
            <b>HSN Code:</b> {hsn_code}<br>
            <b>Description:</b> {self.hsn_map.get(hsn_code, '')}<br>
            <b>Quantity:</b> {qty} {qty_type}<br>
            <b>Taxable Value:</b> ₹{value:.2f}<br>
            <b>Tax Rate:</b> {tax_slab}<br>
            <b>CGST:</b> ₹{cgst:.2f}<br>
            <b>SGST:</b> ₹{sgst:.2f}<br>
            <b>Total Tax:</b> ₹{total_tax:.2f}<br>
            <b>Final Amount:</b> ₹{final_amount:.2f}
            """
            
            self.result_label.setText(result)
            
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values.")
    
    def save_entry(self):
        if not hasattr(self, 'current_entry'):
            QMessageBox.warning(self, "No Data", "Please calculate tax first.")
            return
            
        try:
            path = save_entry(self.current_entry)
            QMessageBox.information(self, "Success", f"Entry saved to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save entry: {str(e)}")
    
    def export_csv(self):
        try:
            if not os.path.exists("data/entries.csv"):
                QMessageBox.warning(self, "No Data", "No entries to export.")
                return
                
            file_path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
            if file_path:
                shutil.copy("data/entries.csv", file_path)
                QMessageBox.information(self, "Success", f"Data exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def sync_to_onedrive(self):
        """Sync data to OneDrive"""
        if not self.user_email:
            QMessageBox.warning(self, "Not Logged In", "Please login with Microsoft to use OneDrive sync")
            return
            
        try:
            if not os.path.exists("data/entries.csv"):
                QMessageBox.warning(self, "No Data", "No entries to sync.")
                return
                
            # Upload to OneDrive
            success = upload_to_onedrive("data/entries.csv", "hsn_data.csv")
            
            if success:
                QMessageBox.information(self, "Success", "Data synced to OneDrive successfully!")
            else:
                QMessageBox.warning(self, "Sync Failed", "Failed to sync data to OneDrive.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"OneDrive sync failed: {str(e)}")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Draw CMYK-style header
        header_height = 60
        width = self.width()
        section_width = width // 4
        
        # Cyan
        painter.fillRect(0, 0, section_width, header_height, QColor(0, 255, 255))
        
        # Magenta
        painter.fillRect(section_width, 0, section_width, header_height, QColor(255, 0, 255))
        
        # Yellow
        painter.fillRect(section_width * 2, 0, section_width, header_height, QColor(255, 255, 0))
        
        # Key (Black)
        painter.fillRect(section_width * 3, 0, section_width, header_height, QColor(0, 0, 0))
        
        # Draw title
        painter.setPen(Qt.white)
        painter.drawText(0, 0, self.width(), header_height, Qt.AlignCenter, "HSN Tax Calculator")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HSNApp()
    window.show()
    sys.exit(app.exec_())