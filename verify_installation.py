#!/usr/bin/env python3
"""Verification script to check if the application is properly installed"""
import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.7+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = ['openpyxl', 'dateutil']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} not installed")
            missing.append(package)
    
    return len(missing) == 0

def check_files():
    """Check if required files exist"""
    files = [
        'main.py',
        'setup.py',
        'requirements.txt',
        'NOUVEAU CODIFICATIO.csv',
        'README.md',
        'QUICKSTART.md',
        'app/__init__.py',
        'app/auth.py',
        'app/gui/login.py',
        'app/gui/dashboard.py',
        'app/gui/insertion.py',
        'app/gui/admin_panel.py',
        'app/gui/report.py',
        'app/models/excel_manager.py',
        'app/utils/csv_parser.py'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    return all_exist

def check_data_files():
    """Check if data files exist"""
    data_files = [
        'data/codification_reference.xlsx',
        'data/rapport_insertions.xlsx'
    ]
    
    all_exist = True
    for file in data_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (run setup.py to create)")
            all_exist = False
    
    return all_exist

def check_data_integrity():
    """Check if data was properly loaded"""
    if not os.path.exists('data/codification_reference.xlsx'):
        return False
    
    sys.path.insert(0, '.')
    try:
        from app.models.excel_manager import ExcelManager
        excel_mgr = ExcelManager()
        data = excel_mgr.load_reference_data()
        
        checks = [
            (len(data['familles']) > 0, "Familles"),
            (len(data['produits']) > 0, "Produits"),
            (len(data['models']) > 0, "Models"),
            (len(data['pannes']) > 0, "Pannes"),
            (len(data['causes']) > 0, "Causes"),
            (len(data['solutions']) > 0, "Solutions"),
            (len(data['users']) > 0, "Users")
        ]
        
        all_ok = True
        for check, name in checks:
            if check:
                print(f"✓ {name} data loaded")
            else:
                print(f"✗ {name} data missing")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"✗ Error checking data: {e}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("SAV Repair Data Management - Installation Verification")
    print("=" * 60)
    print()
    
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("Checking required files...")
    files_ok = check_files()
    print()
    
    print("Checking data files...")
    data_ok = check_data_files()
    print()
    
    if data_ok:
        print("Checking data integrity...")
        integrity_ok = check_data_integrity()
        print()
    else:
        integrity_ok = False
    
    print("=" * 60)
    if python_ok and deps_ok and files_ok and data_ok and integrity_ok:
        print("✅ All checks passed! Application is ready to run.")
        print()
        print("To start the application:")
        print("  python3 main.py")
        print()
        print("Default credentials:")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        if not deps_ok:
            print("Install dependencies with:")
            print("  pip install -r requirements.txt")
            print()
        if not data_ok or not integrity_ok:
            print("Initialize the database with:")
            print("  python3 setup.py")
            print()
    print("=" * 60)

if __name__ == '__main__':
    main()
