# User Accounts

## Default Accounts

The SAV Repair Data Management Application comes with **two pre-configured user accounts**:

### 1. Admin Account

**Credentials:**
- **Username**: `admin`
- **Password**: `admin123`

**Permissions:**
- ✅ View all repair insertions
- ✅ Create new repair records
- ✅ Export monthly reports
- ✅ Access Admin Panel
- ✅ Full CRUD operations on all reference data:
  - Manage product families
  - Manage product types
  - Manage models
  - Manage fault types (pannes)
  - Manage causes
  - Manage solutions
  - Manage service centers
  - Manage user accounts
- ✅ Create new user accounts
- ✅ Reset user passwords
- ✅ Delete user accounts

### 2. Inserter Account

**Credentials:**
- **Username**: `inserter`
- **Password**: `inserter123`

**Permissions:**
- ✅ View all repair insertions
- ✅ Create new repair records
- ✅ Export monthly reports
- ❌ Cannot access Admin Panel
- ❌ Cannot modify reference data
- ❌ Cannot manage user accounts

## Login Instructions

1. Run the application:
   ```bash
   python3 main.py
   ```

2. The login screen will appear

3. Enter credentials for the account you want to use:
   - For full administrative access: use **admin/admin123**
   - For data entry only: use **inserter/inserter123**

4. Click "Login"

## Creating Additional Accounts

Only the **admin** user can create additional accounts:

1. Login as admin
2. Click "Admin Panel"
3. Navigate to the "Users" tab
4. Click "Add User"
5. Enter:
   - Username
   - Password
   - Role (admin or inserter)
6. Click "Save All Changes"

## Resetting Passwords

Only the **admin** user can reset passwords:

1. Login as admin
2. Click "Admin Panel"
3. Navigate to the "Users" tab
4. Select the user whose password needs to be reset
5. Click "Reset Password"
6. Enter the new password
7. Click "Save All Changes"

## Security Notes

⚠️ **Important Security Information:**

- Passwords are currently stored in **plain text** in the Excel file
- This is acceptable for internal use only
- For production environments with sensitive data, consider:
  - Implementing password hashing (bcrypt, argon2)
  - Adding password complexity requirements
  - Implementing account lockout after failed attempts
  - Adding audit logging for user actions

## Changing Default Passwords

**It is strongly recommended to change the default passwords after first login:**

1. Login as admin
2. Go to Admin Panel → Users tab
3. Select the admin account
4. Click "Reset Password"
5. Enter a new, strong password
6. Repeat for the inserter account

## Account Testing

To verify both accounts are working:

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from app.auth import AuthManager

auth_mgr = AuthManager()

# Test admin
user = auth_mgr.authenticate('admin', 'admin123')
print(f"Admin login: {'✓' if user else '✗'}")

# Test inserter
auth_mgr.logout()
user = auth_mgr.authenticate('inserter', 'inserter123')
print(f"Inserter login: {'✓' if user else '✗'}")
EOF
```

Expected output:
```
Admin login: ✓
Inserter login: ✓
```

## Troubleshooting

### Cannot login with default credentials

If the default accounts don't work:

1. Verify the database was initialized:
   ```bash
   python3 verify_installation.py
   ```

2. Re-run the setup to recreate accounts:
   ```bash
   python3 setup.py
   ```

3. Manually add the inserter account if needed:
   ```bash
   python3 add_inserter_account.py
   ```

### Forgot admin password

If you've changed the admin password and forgot it:

1. You'll need to manually edit the Excel file
2. Open `data/codification_reference.xlsx`
3. Go to the "Users" sheet
4. Find the admin user row
5. Change the password column to `admin123`
6. Save and close the Excel file
7. Login with admin/admin123
8. Change to a new password via the Admin Panel

---

**Both accounts are ready to use!** 🎉
