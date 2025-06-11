import PyInstaller.__main__
import os

# Create the spec file first
PyInstaller.__main__.run([
    'main.py',
    '--name=HSN_Tax_Calculator',
    '--windowed',  # No console window
    '--onefile',   # Single executable file
    '--icon=NONE', # Replace with path to your icon if you have one
    '--add-data=HSN_SAC.xlsx;.',  # Include the Excel file
    '--add-data=.env;.'  # Include the .env file
])

print("Executable created successfully in the dist folder!")