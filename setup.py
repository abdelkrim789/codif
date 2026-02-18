#!/usr/bin/env python3
"""Setup script to initialize the application"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.csv_parser import parse_csv_and_populate

def main():
    """Initialize the application"""
    print("=" * 60)
    print("SAV Repair Data Management Application - Setup")
    print("=" * 60)
    print()
    
    # Check if data files already exist
    if os.path.exists('data/codification_reference.xlsx'):
        response = input("Reference file already exists. Recreate? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled. Using existing data files.")
            return
    
    print("Initializing database from CSV file...")
    print()
    
    success = parse_csv_and_populate()
    
    if success:
        print()
        print("=" * 60)
        print("Setup completed successfully!")
        print("=" * 60)
        print()
        print("To start the application, run:")
        print("  python3 main.py")
        print()
        print("Default login credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print()
    else:
        print()
        print("Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
