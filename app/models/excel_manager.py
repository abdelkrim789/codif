"""Excel file manager for reading and writing codification data"""
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime


class ExcelManager:
    """Manages reading and writing to Excel files"""
    
    def __init__(self, base_path='data'):
        self.base_path = base_path
        self.reference_file = os.path.join(base_path, 'codification_reference.xlsx')
        self.rapport_file = os.path.join(base_path, 'rapport_insertions.xlsx')
    
    def create_reference_file(self):
        """Create the codification reference Excel file with all required sheets"""
        wb = Workbook()
        
        # Remove default sheet
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        
        # Create sheets
        wb.create_sheet('Familles')
        wb.create_sheet('Produits')
        wb.create_sheet('Models')
        wb.create_sheet('Pannes')
        wb.create_sheet('Causes')
        wb.create_sheet('Solutions')
        wb.create_sheet('PDR')
        wb.create_sheet('Centres')
        wb.create_sheet('Users')
        
        # Setup Familles sheet
        ws_familles = wb['Familles']
        ws_familles.append(['ID', 'Famille'])
        
        # Setup Produits sheet
        ws_produits = wb['Produits']
        ws_produits.append(['ID', 'Famille_ID', 'Produit'])
        
        # Setup Models sheet
        ws_models = wb['Models']
        ws_models.append(['ID', 'Produit_ID', 'Model'])
        
        # Setup Pannes sheet
        ws_pannes = wb['Pannes']
        ws_pannes.append(['ID', 'Code', 'Produit_ID', 'Panne'])
        
        # Setup Causes sheet
        ws_causes = wb['Causes']
        ws_causes.append(['ID', 'Code', 'Panne_ID', 'Cause'])
        
        # Setup Solutions sheet
        ws_solutions = wb['Solutions']
        ws_solutions.append(['ID', 'Code', 'Cause_ID', 'Solution'])
        
        # Setup PDR sheet
        ws_pdr = wb['PDR']
        ws_pdr.append(['ID', 'Code', 'PDR'])
        
        # Setup Centres sheet
        ws_centres = wb['Centres']
        ws_centres.append(['ID', 'Centre'])
        
        # Setup Users sheet
        ws_users = wb['Users']
        ws_users.append(['ID', 'Username', 'Password', 'Role'])
        # Add default admin account
        ws_users.append([1, 'admin', 'admin123', 'admin'])
        
        wb.save(self.reference_file)
        return wb
    
    def create_rapport_file(self):
        """Create the rapport insertions Excel file"""
        wb = Workbook()
        ws = wb.active
        ws.title = 'Insertions'
        
        # Setup headers
        headers = ['#', 'Client', 'Produit', 'Type de produit', 'N° de série', 
                   'Garantie', 'Date produit', 'Panne', 'Réparation effectuée', 
                   'PDR consommée', 'Statut', 'Centre', 'Date réception', 'Date réparation']
        
        ws.append(headers)
        
        # Style the headers
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Enable auto-filter
        ws.auto_filter.ref = ws.dimensions
        
        wb.save(self.rapport_file)
        return wb
    
    def load_reference_data(self):
        """Load all reference data from Excel file"""
        if not os.path.exists(self.reference_file):
            return None
        
        wb = load_workbook(self.reference_file)
        data = {}
        
        # Load Familles
        data['familles'] = []
        ws = wb['Familles']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['familles'].append({'id': row[0], 'famille': row[1]})
        
        # Load Produits
        data['produits'] = []
        ws = wb['Produits']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['produits'].append({'id': row[0], 'famille_id': row[1], 'produit': row[2]})
        
        # Load Models
        data['models'] = []
        ws = wb['Models']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['models'].append({'id': row[0], 'produit_id': row[1], 'model': row[2]})
        
        # Load Pannes
        data['pannes'] = []
        ws = wb['Pannes']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['pannes'].append({'id': row[0], 'code': row[1], 'produit_id': row[2], 'panne': row[3]})
        
        # Load Causes
        data['causes'] = []
        ws = wb['Causes']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['causes'].append({'id': row[0], 'code': row[1], 'panne_id': row[2], 'cause': row[3]})
        
        # Load Solutions
        data['solutions'] = []
        ws = wb['Solutions']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['solutions'].append({'id': row[0], 'code': row[1], 'cause_id': row[2], 'solution': row[3]})
        
        # Load PDR
        data['pdr'] = []
        ws = wb['PDR']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['pdr'].append({'id': row[0], 'code': row[1], 'pdr': row[2]})
        
        # Load Centres
        data['centres'] = []
        ws = wb['Centres']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['centres'].append({'id': row[0], 'centre': row[1]})
        
        # Load Users
        data['users'] = []
        ws = wb['Users']
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                data['users'].append({'id': row[0], 'username': row[1], 'password': row[2], 'role': row[3]})
        
        wb.close()
        return data
    
    def save_reference_data(self, data):
        """Save reference data to Excel file"""
        wb = load_workbook(self.reference_file)
        
        # Save Familles
        ws = wb['Familles']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('familles', []):
            ws.append([item['id'], item['famille']])
        
        # Save Produits
        ws = wb['Produits']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('produits', []):
            ws.append([item['id'], item['famille_id'], item['produit']])
        
        # Save Models
        ws = wb['Models']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('models', []):
            ws.append([item['id'], item['produit_id'], item['model']])
        
        # Save Pannes
        ws = wb['Pannes']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('pannes', []):
            ws.append([item['id'], item['code'], item['produit_id'], item['panne']])
        
        # Save Causes
        ws = wb['Causes']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('causes', []):
            ws.append([item['id'], item['code'], item['panne_id'], item['cause']])
        
        # Save Solutions
        ws = wb['Solutions']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('solutions', []):
            ws.append([item['id'], item['code'], item['cause_id'], item['solution']])
        
        # Save PDR
        ws = wb['PDR']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('pdr', []):
            ws.append([item['id'], item['code'], item['pdr']])
        
        # Save Centres
        ws = wb['Centres']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('centres', []):
            ws.append([item['id'], item['centre']])
        
        # Save Users
        ws = wb['Users']
        ws.delete_rows(2, ws.max_row)
        for item in data.get('users', []):
            ws.append([item['id'], item['username'], item['password'], item['role']])
        
        wb.save(self.reference_file)
        wb.close()
    
    def load_insertions(self):
        """Load all insertions from rapport file"""
        if not os.path.exists(self.rapport_file):
            return []
        
        wb = load_workbook(self.rapport_file)
        ws = wb['Insertions']
        
        insertions = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                insertions.append({
                    'num': row[0],
                    'client': row[1],
                    'produit': row[2],
                    'type_produit': row[3],
                    'num_serie': row[4],
                    'garantie': row[5],
                    'date_produit': row[6],
                    'panne': row[7],
                    'reparation': row[8],
                    'pdr': row[9],
                    'statut': row[10],
                    'centre': row[11],
                    'date_reception': row[12],
                    'date_reparation': row[13]
                })
        
        wb.close()
        return insertions
    
    def add_insertion(self, insertion_data):
        """Add a new insertion to the rapport file"""
        wb = load_workbook(self.rapport_file)
        ws = wb['Insertions']
        
        # Get next row number
        next_num = ws.max_row
        
        ws.append([
            next_num,
            insertion_data.get('client'),
            insertion_data.get('produit'),
            insertion_data.get('type_produit'),
            insertion_data.get('num_serie'),
            insertion_data.get('garantie'),
            insertion_data.get('date_produit'),
            insertion_data.get('panne'),
            insertion_data.get('reparation'),
            insertion_data.get('pdr'),
            insertion_data.get('statut'),
            insertion_data.get('centre'),
            insertion_data.get('date_reception'),
            insertion_data.get('date_reparation')
        ])
        
        wb.save(self.rapport_file)
        wb.close()
