import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, 
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                             QMessageBox, QFileDialog, QDesktopWidget)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

# Load HSN codes from Excel
def load_hsn_codes():
    try:
        df = pd.read_excel("HSN_SAC.xlsx")
        codes = df['HSN_CD'].astype(str).tolist()
        return codes, df.set_index('HSN_CD')['HSN_Description'].to_dict()
    except Exception as e:
        print(f"Error loading HSN data: {e}")
        # Return sample data as fallback
        sample_codes = ['0101', '0102', '0201', '0202', '0301']
        sample_map = {
            '0101': 'Live horses',
            '0102': 'Live bovine animals',
            '0201': 'Meat of bovine animals, fresh',
            '0202': 'Meat of bovine animals, frozen',
            '0301': 'Live fish'
        }
        return sample_codes, sample_map

# Tax calculation logic
def calculate_tax(base_value, slab):
    slab_map = {
        "0%": (0.0, 0.0),
        "0.25%": (0.125, 0.125),
        "3%": (1.5, 1.5),
        "5%": (2.5, 2.5),
        "12%": (6.0, 6.0),
        "18%": (9.0, 9.0),
        "28%": (14.0, 14.0)
    }
    cgst, sgst = slab_map.get(slab, (0.0, 0.0))
    return base_value * (cgst / 100), base_value * (sgst / 100)

# Save entry to CSV
def save_entry(entry):
    path = "data/entries.csv"
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame([entry])
    if os.path.exists(path):
        df.to_csv(path, mode='a', header=False, index=False)
    else:
        df.to_csv(path, index=False)
    return path

class HSNApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HSN Tax Calculator")
        self.setGeometry(100, 100, 1080, 720)
        self.center_screen()
        
        # Load HSN data
        self.hsn_codes, self.hsn_map = load_hsn_codes()
        
        self.initUI()
        
    def center_screen(self):
        # Center window on screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def initUI(self):
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
                'FinalAmount': final_amount
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
                import shutil
                shutil.copy("data/entries.csv", file_path)
                QMessageBox.information(self, "Success", f"Data exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
        
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