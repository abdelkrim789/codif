# SAV Repair Data Management Application

A Python desktop application for managing after-sales service (SAV) repair data for appliances. This application eliminates data inconsistencies by enforcing standardized data entry through cascading dropdowns.

## Features

- **User Authentication**: Role-based access control (Admin and Inserter roles)
- **Cascading Dropdowns**: Prevents data inconsistencies by forcing selection from predefined options
- **CRUD Operations**: Full management of codification data (Admin only)
- **Data Insertion**: Easy-to-use form for adding repair records
- **Report Generation**: Export formatted monthly reports
- **Excel-Based Storage**: No external database required

## Architecture

The application uses two Excel files:

1. **codification_reference.xlsx** - Reference database containing:
   - Product families (Familles de produit)
   - Product types (Produits)
   - Models
   - Faults (Pannes) with codes
   - Causes with codes
   - Solutions with codes
   - Spare parts (PDR) with codes
   - Service centers (Centres)
   - User accounts

2. **rapport_insertions.xlsx** - Daily insertions and monthly reports containing repair records

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/abdelkrim789/codif.git
cd codif
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database (first time only):
```bash
python3 setup.py
```

This will:
- Parse the `NOUVEAU CODIFICATIO.csv` file
- Create `data/codification_reference.xlsx` with pre-loaded FROID family data
- Create `data/rapport_insertions.xlsx` template
- Set up the default admin account

4. (Optional) Add sample data for testing:
```bash
python3 add_sample_data.py
```

This will add 10 sample repair insertions to test the dashboard and report features.

## Usage

### Starting the Application

Run the main application:
```bash
python3 main.py
```

### Default Login Credentials

The system comes with two pre-configured accounts:

#### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Admin

#### Inserter Account
- **Username**: `inserter`
- **Password**: `inserter123`
- **Role**: Inserter

### User Roles

#### Admin
- Full access to CRUD operations for all entities
- Can manage user accounts (create, reset passwords)
- Can view all inserted data
- Can insert new repair records
- Can export reports

#### Inserter
- Can insert new repair records
- Can view existing data
- Cannot modify codification reference data

### Cascading Dropdown Flow

The application ensures data consistency through cascading dropdowns:

1. **Famille de produit** → Select product family (e.g., FROID)
2. **Produit** → Select product type (e.g., RÉFRIGÉRATEUR)
3. **Model** → Select specific model (e.g., GN-BCD525)
4. **Panne** → Select fault type (e.g., PAS DE FROID)
5. **Cause** → Select cause (e.g., COMPRESSEUR)
6. **Solution** → Auto-fills based on cause (e.g., CHANGE COMPRESSEUR)
7. **PDR** → Select spare part used

Each selection filters the next dropdown to show only related options.

### Pre-loaded Data

The application comes pre-loaded with codification data for the **FROID** (Cold) product family:

#### Product Types:
1. **RÉFRIGÉRATEUR** (Refrigerator)
   - Models: GN-BCD525, GN-BCD435, GRF-D500, GN-MBM-92, GN-MBM-60
   
2. **CONGÉLATEUR** (Freezer)
   - Models: GN-BD(W)-453, GN-BD(W)-420, GN-BD(W)-247, GN-BD(W)-170, GN-BD(W)-140, GN-CFH-330, GN-CFH-260, GN-CPF180, CG-CF330F-B, CG-CF270F-B, GN-CFH180B, GN-SCSD(W)390, CG-CF130F-G, GN-CPF-358, GN-CFH-400
   
3. **RÉFRIGÉRATEUR PRÉSENTOIR** (Display Refrigerator)
   - Models: GN-KBC98N, GN-KBC131N
   
4. **FONTAINE FRAÎCHE** (Water Fountain)
   - Models: ge-ffjx12-brf, ge-ffjx15-b

#### Common Faults:
- **PAS DE FROID** - No cooling
- **BRUIT** - Noise
- **GIVRE** - Frost/ice buildup
- **FUITE D'EAU** - Water leakage (Fountain only)
- **ARRÊT TOTAL** - Complete shutdown (Fountain only)
- **PAS DE CHAUD** - No heating (Fountain only)
- **L'EAU NE COULE PAS** - Water not flowing (Fountain only)

**Note**: RÉFRIGÉRATEUR NO FROST INVERTER product type is intentionally left empty for admin to populate later via CRUD operations.

## Admin Panel

The admin panel provides tabs for managing:

- **Familles**: Product families
- **Produits**: Product types
- **Models**: Specific models
- **Pannes**: Fault types with codes
- **Causes**: Fault causes with codes
- **Solutions**: Solutions with codes
- **Centres**: Service centers
- **Users**: User accounts (create, reset passwords)

### Adding New Data

1. Navigate to the appropriate tab
2. Click "Add" button
3. Enter required information
4. Click "Save All Changes" to persist

### Managing Users

Admin can:
- Add new inserter accounts
- Reset passwords for any user
- Delete user accounts (except admin)

## Report Generation

Click "Export Report" to generate a formatted monthly report with:
- Header section with center name and month
- All repair insertions
- Professional formatting
- Auto-filters enabled

Reports are saved as `rapport_[Month]_[Year].xlsx` in the `data/` directory.

## File Structure

```
codif/
├── main.py                          # Application entry point
├── app/
│   ├── __init__.py
│   ├── auth.py                      # Authentication logic
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── login.py                 # Login screen
│   │   ├── dashboard.py             # Main dashboard
│   │   ├── insertion.py             # Data insertion form
│   │   ├── admin_panel.py           # CRUD management
│   │   └── report.py                # Report generation
│   ├── models/
│   │   ├── __init__.py
│   │   └── excel_manager.py         # Excel read/write operations
│   └── utils/
│       ├── __init__.py
│       └── csv_parser.py            # CSV parsing utility
├── data/
│   ├── codification_reference.xlsx  # Reference database
│   └── rapport_insertions.xlsx      # Repair insertions
├── NOUVEAU CODIFICATIO.csv          # Source data
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Technical Stack

- **Python 3**: Core programming language
- **tkinter**: GUI framework (built-in with Python)
- **openpyxl**: Excel file manipulation
- **python-dateutil**: Date handling

## Troubleshooting

### "Module not found" errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Excel files not found
Run the CSV parser to initialize the database:
```bash
python3 -c "
import sys
sys.path.insert(0, '.')
exec(open('app/utils/csv_parser.py').read())
"
```

### Can't login
Use the default credentials:
- Username: `admin`
- Password: `admin123`

### Cascading dropdowns not working
Ensure you're selecting options in order:
1. Famille → 2. Produit → 3. Model → 4. Panne → 5. Cause

## Development

### Adding New Product Families

1. Login as admin
2. Go to Admin Panel
3. Navigate to "Familles" tab
4. Click "Add" and enter family name
5. Add products, models, pannes, causes, and solutions
6. Save changes

### Customizing the Application

- Modify GUI layouts in `app/gui/` files
- Update Excel operations in `app/models/excel_manager.py`
- Add new features following the existing structure

## Security Notes

- Passwords are stored in plain text in the Excel file (for simplicity)
- In a production environment, implement proper password hashing
- Consider adding backup functionality
- Implement data validation and sanitization

## License

This project is created for internal use at Géant Froid SAV.

## Support

For issues or questions, contact the SAV administration.
