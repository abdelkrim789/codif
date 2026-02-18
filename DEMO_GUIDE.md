# Application Demo Guide

This guide demonstrates the key features of the SAV Repair Data Management Application.

## 📱 Application Screens

### 1. Login Screen
```
┌─────────────────────────────────────┐
│  SAV Repair Data Management         │
│                                     │
│  Username: [________________]       │
│                                     │
│  Password: [________________]       │
│                                     │
│          [    Login    ]            │
│                                     │
└─────────────────────────────────────┘

Default accounts available:
- Admin: username=admin, password=admin123
- Inserter: username=inserter, password=inserter123
```

### 2. Main Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│ SAV Repair Data Management System            User: admin (ADMIN)   │
├─────────────────────────────────────────────────────────────────────┤
│ [➕ New Insertion] [🔄 Refresh] [📊 Export] [⚙️ Admin Panel]        │
├─────────────────────────────────────────────────────────────────────┤
│ # │Client  │Produit │Model    │Série  │Panne      │Statut │...    │
├───┼────────┼────────┼─────────┼───────┼───────────┼───────┼───────┤
│ 1 │Ahmed   │RÉFRIG. │GN-BCD525│SN1234 │PAS FROID  │Réparé │...    │
│ 2 │Fatima  │CONGÉL. │GN-BD420 │SN5678 │BRUIT      │En cours│...   │
│ 3 │Omar    │FONTAINE│ge-ffjx12│SN9012 │FUITE EAU  │Réparé │...    │
├───┴────────┴────────┴─────────┴───────┴───────────┴───────┴───────┤
│ Status: Loaded 3 insertions                                         │
└─────────────────────────────────────────────────────────────────────┘
```

### 3. New Insertion Form
```
┌─────────────────────────────────────┐
│     New Repair Insertion            │
├─────────────────────────────────────┤
│                                     │
│ Client:           [Mohamed Ali   ]  │
│                                     │
│ Famille:          [FROID        ▼]  │
│                                     │
│ Produit:          [RÉFRIGÉRATEUR▼]  │
│                                     │
│ Type de produit:  [GN-BCD525    ▼]  │
│                                     │
│ N° de série:      [SN-12345      ]  │
│                                     │
│ Garantie:         [Garantie     ▼]  │
│                                     │
│ Date produit:     [2024-01-15    ]  │
│                                     │
│ Panne:            [PAS DE FROID ▼]  │
│                                     │
│ Cause:            [COMPRESSEUR  ▼]  │
│                                     │
│ Réparation:       [CHANGE COMPRES...│ ← Auto-filled!
│                                     │
│ PDR consommée:    [PDR-123      ▼]  │
│                                     │
│ Statut:           [Réparé       ▼]  │
│                                     │
│ Centre:           [Centre Prin. ▼]  │
│                                     │
│ Date réception:   [2024-02-01    ]  │
│                                     │
│ Date réparation:  [2024-02-05    ]  │
│                                     │
│    [   Save   ]  [  Cancel  ]       │
│                                     │
└─────────────────────────────────────┘
```

### 4. Admin Panel
```
┌───────────────────────────────────────────────────────────────────┐
│                     Administration Panel                          │
├───────────────────────────────────────────────────────────────────┤
│ [Familles][Produits][Models][Pannes][Causes][Solutions][Users]   │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Currently viewing: Produits                                      │
│  [Add] [Delete]                                                   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ ID │ Famille_ID │ Produit                │                  │ │
│  ├────┼────────────┼────────────────────────┤                  │ │
│  │ 1  │ 1          │ RÉFRIGÉRATEUR          │                  │ │
│  │ 2  │ 1          │ CONGÉLATEUR            │                  │ │
│  │ 3  │ 1          │ RÉFRIGÉRATEUR PRÉSENTOIR│                 │ │
│  │ 4  │ 1          │ FONTAINE FRAÎCHE       │                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│           [Save All Changes]  [Close]                             │
└───────────────────────────────────────────────────────────────────┘
```

### 5. Generated Report
```
Excel File: rapport_February_2024.xlsx

┌────────────────────────────────────────────────────────────────────┐
│              Direction SAV Géant Froid                             │
│              Centre SAV Centre Principal                           │
│              Rapport Mois February 2024                            │
├──┬──────────┬────────────┬──────────┬────────┬──────────┬─────────┤
│#│Client    │Produit     │Type      │N° série│Garantie  │Date...  │
├──┼──────────┼────────────┼──────────┼────────┼──────────┼─────────┤
│1│Ahmed     │RÉFRIGÉRATEUR│GN-BCD525│SN12345 │Garantie  │2024-... │
│2│Fatima    │CONGÉLATEUR  │GN-BD420 │SN5678  │Hors Gar. │2024-... │
└──┴──────────┴────────────┴──────────┴────────┴──────────┴─────────┘
  (Continues with more columns: Panne, Réparation, PDR, Statut, etc.)
  
  Features:
  ✓ Professional formatting
  ✓ Bold headers with blue background
  ✓ Auto-filters enabled
  ✓ Proper column widths
  ✓ Borders on all cells
```

## 🎬 Demo Scenarios

### Scenario 1: Adding a Refrigerator Repair

1. **Login** as admin
2. **Click** "New Insertion"
3. **Enter** client name: "Hassan Boutayeb"
4. **Select** cascading options:
   - Famille: FROID
   - Produit: RÉFRIGÉRATEUR
   - Model: GN-BCD525
   - Panne: PAS DE FROID
   - Cause: COMPRESSEUR
   - ✨ Solution auto-fills: "CHANGE COMPRESSEUR"
5. **Fill** remaining fields:
   - Serial: SN-67890
   - Garantie: Garantie
   - Status: Réparé
   - Centre: Centre Principal
6. **Click** Save
7. **See** new record in dashboard

### Scenario 2: Creating a New User (Admin)

1. **Open** Admin Panel
2. **Go to** Users tab
3. **Click** "Add User"
4. **Enter** details:
   - Username: inserter1
   - Password: pass123
   - Role: inserter
5. **Click** "Save All Changes"
6. **Logout** and login as inserter1
7. **Notice** Admin Panel button is hidden

### Scenario 3: Adding a New Model (Admin)

1. **Open** Admin Panel
2. **Go to** Models tab
3. **Click** "Add"
4. **Enter**:
   - Produit ID: 1 (RÉFRIGÉRATEUR)
   - Model: GN-NEW-MODEL
5. **Click** "Save All Changes"
6. **Test**: Create new insertion
7. **Verify**: New model appears in dropdown

### Scenario 4: Generating Monthly Report

1. **Add** several insertions (or use sample data)
2. **Click** "Export Report" on dashboard
3. **Check** data/ folder for new file:
   - `rapport_February_2024.xlsx`
4. **Open** in Excel
5. **See** professional formatting:
   - Header with center name
   - Blue header row
   - All data properly formatted
   - Auto-filters enabled

## 🔍 Key Features Demonstration

### Cascading Dropdowns in Action

```
Step 1: Select Famille
┌─────────────────┐
│ FROID        ▼ │ → Filters Produits
└─────────────────┘

Step 2: Select Produit
┌─────────────────┐
│ RÉFRIGÉRATEUR▼ │ → Filters Models & Pannes
└─────────────────┘

Step 3: Select Model
┌─────────────────┐
│ GN-BCD525    ▼ │ → Keeps Pannes for this Produit
└─────────────────┘

Step 4: Select Panne
┌─────────────────┐
│ PAS DE FROID ▼ │ → Filters Causes
└─────────────────┘

Step 5: Select Cause
┌─────────────────┐
│ COMPRESSEUR  ▼ │ → Auto-fills Solution!
└─────────────────┘

Result: Réparation effectuée
┌─────────────────────────┐
│ CHANGE COMPRESSEUR      │ ✓ Automatically filled!
└─────────────────────────┘
```

### Data Consistency Example

**Before (Manual Entry):**
```
- "pas de lavage"
- "non lavage"
- "Pas de lavage"
- "PAS LAVAGE"
→ 4 different ways = Inconsistent data! ❌
```

**After (Cascading Dropdowns):**
```
- "PAS DE FROID"
- "PAS DE FROID"
- "PAS DE FROID"
- "PAS DE FROID"
→ Always consistent! ✅
```

## 🎯 Testing Checklist

Use this checklist to test all features:

### Authentication
- [ ] Login with admin/admin123
- [ ] Login with invalid credentials (should fail)
- [ ] Logout and login again

### Dashboard
- [ ] View empty dashboard
- [ ] Add insertion and refresh
- [ ] View populated dashboard
- [ ] Check all columns display correctly

### Insertion Form
- [ ] Open new insertion form
- [ ] Test cascading dropdowns (Famille → Produit → Model → Panne → Cause)
- [ ] Verify solution auto-fills
- [ ] Save insertion
- [ ] Cancel insertion

### Admin Panel (Admin Only)
- [ ] Open admin panel
- [ ] Navigate through all tabs
- [ ] Add a famille
- [ ] Add a produit
- [ ] Add a model
- [ ] Add a panne
- [ ] Add a cause
- [ ] Add a solution
- [ ] Add a centre
- [ ] Add a user
- [ ] Reset user password
- [ ] Delete an item
- [ ] Save all changes

### Report Generation
- [ ] Add multiple insertions
- [ ] Click "Export Report"
- [ ] Verify file created in data/
- [ ] Open Excel file
- [ ] Check formatting

### Role Testing
- [ ] Login as inserter
- [ ] Verify Admin Panel button hidden
- [ ] Try to add insertion (should work)
- [ ] Verify can't access CRUD operations

## 📊 Sample Data

Run `python3 add_sample_data.py` to generate 10 sample insertions with:
- Random clients
- Random product types
- Random faults
- Random dates
- Random statuses

Perfect for testing and demonstrations!

---

**Ready to demonstrate? Follow the scenarios above!** 🎉
