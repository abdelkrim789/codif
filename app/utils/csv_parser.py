"""Parse CSV file and populate the reference Excel file"""
import csv
import os
import sys
from app.models.excel_manager import ExcelManager


def parse_csv_and_populate():
    """Parse the NOUVEAU CODIFICATIO.csv and populate reference Excel"""
    csv_file = 'NOUVEAU CODIFICATIO.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return False
    
    # Initialize data structures
    data = {
        'familles': [],
        'produits': [],
        'models': [],
        'pannes': [],
        'causes': [],
        'solutions': [],
        'pdr': [],
        'centres': [],
        'users': []
    }
    
    # Counters for IDs
    famille_id = 1
    produit_id = 1
    model_id = 1
    panne_id = 1
    cause_id = 1
    solution_id = 1
    pdr_id = 1
    centre_id = 1
    
    # Maps for lookups
    famille_map = {}
    produit_map = {}
    model_map = {}
    panne_map = {}
    cause_map = {}
    
    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Add FROID famille
    data['familles'].append({'id': famille_id, 'famille': 'FROID'})
    famille_map['FROID'] = famille_id
    famille_id += 1
    
    current_produit = None
    current_produit_id = None
    current_model = None
    current_model_id = None
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        # Skip empty rows
        if not any(row):
            i += 1
            continue
        
        # Check for product type header (in column 2)
        if len(row) > 2 and row[2]:
            produit_name = row[2].strip()
            
            # Skip the incomplete section
            if 'NO FROST INVERTER' in produit_name.upper():
                break
            
            # Check if this is a product type header
            if produit_name.upper() in ['REFREGERATEUR', 'CONGELATEUR', 'REFREGERATEUR PRESONTOIR', 'FONAINE FRECH']:
                # Normalize product names
                if 'REFREGERATEUR PRESONTOIR' in produit_name.upper():
                    produit_name = 'RÉFRIGÉRATEUR PRÉSENTOIR'
                elif 'REFREGERATEUR' in produit_name.upper():
                    produit_name = 'RÉFRIGÉRATEUR'
                elif 'CONGELATEUR' in produit_name.upper():
                    produit_name = 'CONGÉLATEUR'
                elif 'FONAINE FRECH' in produit_name.upper():
                    produit_name = 'FONTAINE FRAÎCHE'
                
                current_produit = produit_name
                
                # Check if this produit already exists
                if current_produit not in produit_map:
                    data['produits'].append({
                        'id': produit_id,
                        'famille_id': famille_map['FROID'],
                        'produit': current_produit
                    })
                    produit_map[current_produit] = produit_id
                    current_produit_id = produit_id
                    produit_id += 1
                else:
                    current_produit_id = produit_map[current_produit]
                
                i += 1
                continue
            
            # Check if this is a model name
            elif current_produit and row[2] and row[3]:
                model_name = row[2].strip()
                
                # Check if next column has panne code
                if row[3].strip() and ('-' in row[3].strip() or row[3].strip().startswith('REF') or 
                                        row[3].strip().startswith('CON') or row[3].strip().startswith('FON')):
                    current_model = model_name
                    
                    # Check if model already exists
                    model_key = f"{current_produit_id}_{current_model}"
                    if model_key not in model_map:
                        data['models'].append({
                            'id': model_id,
                            'produit_id': current_produit_id,
                            'model': current_model
                        })
                        model_map[model_key] = model_id
                        current_model_id = model_id
                        model_id += 1
                    else:
                        current_model_id = model_map[model_key]
        
        # Parse panne/cause/solution rows
        if len(row) > 8 and row[3] and row[4] and current_produit_id:
            panne_code = row[3].strip()
            panne_name = row[4].strip()
            cause_code = row[5].strip() if len(row) > 5 else ''
            cause_name = row[6].strip() if len(row) > 6 else ''
            solution_code = row[7].strip() if len(row) > 7 else ''
            solution_name = row[8].strip() if len(row) > 8 else ''
            
            # Skip header rows
            if panne_code.upper() == 'CODE PANNE' or panne_name.upper() == 'PANNE':
                i += 1
                continue
            
            # Check if this is a valid panne row
            if panne_code and panne_name and cause_code and cause_name:
                # Add panne if not exists
                panne_key = f"{current_produit_id}_{panne_name}"
                if panne_key not in panne_map:
                    data['pannes'].append({
                        'id': panne_id,
                        'code': panne_code,
                        'produit_id': current_produit_id,
                        'panne': panne_name
                    })
                    panne_map[panne_key] = panne_id
                    current_panne_id = panne_id
                    panne_id += 1
                else:
                    current_panne_id = panne_map[panne_key]
                
                # Add cause
                cause_key = f"{current_panne_id}_{cause_name}"
                if cause_key not in cause_map:
                    data['causes'].append({
                        'id': cause_id,
                        'code': cause_code,
                        'panne_id': current_panne_id,
                        'cause': cause_name
                    })
                    cause_map[cause_key] = cause_id
                    current_cause_id = cause_id
                    cause_id += 1
                else:
                    current_cause_id = cause_map[cause_key]
                
                # Add solution
                if solution_code and solution_name:
                    data['solutions'].append({
                        'id': solution_id,
                        'code': solution_code,
                        'cause_id': current_cause_id,
                        'solution': solution_name
                    })
                    solution_id += 1
        
        i += 1
    
    # Add default admin user
    data['users'].append({
        'id': 1,
        'username': 'admin',
        'password': 'admin123',
        'role': 'admin'
    })
    
    # Create Excel files
    excel_mgr = ExcelManager()
    excel_mgr.create_reference_file()
    excel_mgr.save_reference_data(data)
    excel_mgr.create_rapport_file()
    
    print(f"Successfully populated reference file with:")
    print(f"  - {len(data['familles'])} familles")
    print(f"  - {len(data['produits'])} produits")
    print(f"  - {len(data['models'])} models")
    print(f"  - {len(data['pannes'])} pannes")
    print(f"  - {len(data['causes'])} causes")
    print(f"  - {len(data['solutions'])} solutions")
    print(f"  - {len(data['users'])} users")
    
    return True


if __name__ == '__main__':
    parse_csv_and_populate()
