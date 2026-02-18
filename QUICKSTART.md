# Quick Start Guide

This guide will help you get started with the SAV Repair Data Management Application.

## Prerequisites

- Python 3.7 or higher installed on your system
- Basic command line knowledge

## Installation (5 minutes)

### 1. Get the Code

```bash
git clone https://github.com/abdelkrim789/codif.git
cd codif
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- openpyxl (for Excel file handling)
- python-dateutil (for date operations)

### 3. Initialize the Database

```bash
python3 setup.py
```

This will:
- Read the CSV file with codification data
- Create the Excel reference database
- Set up the admin account

Expected output:
```
Successfully populated reference file with:
  - 1 familles
  - 4 produits
  - 23 models
  - 15 pannes
  - 68 causes
  - 370 solutions
  - 1 users
```

### 4. (Optional) Add Sample Data

```bash
python3 add_sample_data.py
```

This adds 10 sample repair records for testing.

## Running the Application

```bash
python3 main.py
```

This will open the login window.

## First Login

Use these credentials:
- **Username**: `admin`
- **Password**: `admin123`

## What You'll See

1. **Login Screen**: Enter your credentials
2. **Dashboard**: View all repair insertions in a table
3. **Buttons**:
   - **New Insertion**: Add a new repair record
   - **Refresh**: Reload the data
   - **Export Report**: Generate monthly report
   - **Admin Panel**: Manage reference data (admin only)

## Adding Your First Repair Record

1. Click **"New Insertion"**
2. Fill in the form using the cascading dropdowns:
   - Client: Enter customer name
   - Famille: Select "FROID"
   - Produit: Select product type (e.g., "RÉFRIGÉRATEUR")
   - Type de produit: Select model (e.g., "GN-BCD525")
   - Panne: Select fault (e.g., "PAS DE FROID")
   - Cause: Select cause (e.g., "COMPRESSEUR")
   - Solution is auto-filled!
3. Fill in remaining fields (dates, status, etc.)
4. Click **Save**

## Managing Reference Data (Admin Only)

1. Click **"Admin Panel"**
2. Use the tabs to manage:
   - Familles (Product families)
   - Produits (Product types)
   - Models
   - Pannes (Faults)
   - Causes
   - Solutions
   - Centres (Service centers)
   - Users
3. Click **"Add"** to create new entries
4. Click **"Delete"** to remove selected entry
5. Click **"Save All Changes"** to persist changes

## Creating a New User (Admin Only)

1. Go to **Admin Panel** → **Users** tab
2. Click **"Add User"**
3. Enter:
   - Username
   - Password
   - Role (admin or inserter)
4. Click **"Save All Changes"**

## Generating Reports

1. Click **"Export Report"** on the dashboard
2. A formatted Excel report will be created in the `data/` folder
3. Named as `rapport_[Month]_[Year].xlsx`

## Troubleshooting

### Can't see the GUI?
Make sure you have a graphical environment. The application requires a display to run tkinter.

### "Module not found" errors?
Install dependencies:
```bash
pip install -r requirements.txt
```

### Excel files missing?
Run the setup:
```bash
python3 setup.py
```

### Can't login?
Default credentials are:
- Username: `admin`
- Password: `admin123`

## Next Steps

1. **Add your service centers**: Admin Panel → Centres tab
2. **Create inserter accounts**: Admin Panel → Users tab
3. **Start adding real repair data**: New Insertion button
4. **Customize as needed**: Add new product families, models, etc.

## File Locations

- Excel reference database: `data/codification_reference.xlsx`
- Insertion records: `data/rapport_insertions.xlsx`
- Monthly reports: `data/rapport_[Month]_[Year].xlsx`

## Need Help?

Refer to the full README.md for detailed documentation.

---

**Happy tracking!** 🎉
