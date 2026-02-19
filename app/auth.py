"""Authentication module for user login and session management"""
from app.models.excel_manager import ExcelManager


class AuthManager:
    """Manages user authentication"""
    
    def __init__(self):
        self.excel_mgr = ExcelManager()
        self.current_user = None
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        data = self.excel_mgr.load_reference_data()
        if not data:
            return None
        
        users = data.get('users', [])
        for user in users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return user
        
        return None
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.current_user and self.current_user.get('role') == 'admin'
    
    def is_inserter(self):
        """Check if current user is inserter"""
        return self.current_user and self.current_user.get('role') == 'inserter'
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
