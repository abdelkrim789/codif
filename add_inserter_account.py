#!/usr/bin/env python3
"""Add default inserter account to the system"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.excel_manager import ExcelManager

def add_inserter_account():
    """Add a default inserter account if it doesn't exist"""
    excel_mgr = ExcelManager()
    
    print("=" * 60)
    print("Adding Default Inserter Account")
    print("=" * 60)
    print()
    
    # Load reference data
    data = excel_mgr.load_reference_data()
    
    if not data:
        print("Error: Could not load reference data")
        return False
    
    # Check current users
    print("Current users:")
    for user in data['users']:
        print(f"  - {user['username']} ({user['role']})")
    print()
    
    # Check if inserter already exists
    inserter_exists = any(u['role'] == 'inserter' for u in data['users'])
    
    if inserter_exists:
        print("✓ Inserter account already exists")
        return True
    
    # Add inserter account
    print("Adding default inserter account...")
    new_id = max([u['id'] for u in data['users']], default=0) + 1
    
    new_inserter = {
        'id': new_id,
        'username': 'inserter',
        'password': 'inserter123',
        'role': 'inserter'
    }
    
    data['users'].append(new_inserter)
    
    # Save to Excel
    excel_mgr.save_reference_data(data)
    
    print(f"✓ Created inserter account:")
    print(f"  Username: {new_inserter['username']}")
    print(f"  Password: {new_inserter['password']}")
    print(f"  Role: {new_inserter['role']}")
    print()
    
    # Verify
    data = excel_mgr.load_reference_data()
    print("Updated users list:")
    for user in data['users']:
        print(f"  - {user['username']} ({user['role']})")
    print()
    
    print("=" * 60)
    print("✅ Inserter account added successfully!")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    add_inserter_account()
