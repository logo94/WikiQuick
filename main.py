#!/usr/bin/env python3

# Imports
import os, sys, re, csv, io
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import subprocess
import platform
from typing import Optional
from urllib.parse import unquote 

# Function to format date strings into QuickStatements date format
def format_date(date_string):
    
    # Define possible date formats
    DATE_FORMATS = [
        ('%d-%m-%Y', 11),  # 10-06-2024
        ('%Y-%m-%d', 11),  # 2024-06-10
        ('%Y-%m', 10),     # 2024-06
    ]
    
    clean_date = date_string.strip().replace('/', '-').replace('.', '-')
    
    # Year only
    if re.match(r'^\d{4}$', clean_date):
        year = clean_date
        return f"+{year}-00-00T00:00:00Z/9"
    
    # Year-Month / Year-Month-Day
    dt: Optional[datetime] = None
    precision: int = 11
    
    for fmt, prec in DATE_FORMATS:
        try:
            dt = datetime.strptime(clean_date, fmt)
            precision = prec
            break
        except ValueError:
            continue
    
    if dt is None:
        print(f"ATTENZIONE: Impossibile interpretare la data '{date_string}'. Riga ignorata.")
        return ''
    
    if precision == 11:
        iso_date = f"+{dt.strftime('%Y-%m-%d')}T00:00:00Z/11"
    elif precision == 10:
        iso_date = f"+{dt.strftime('%Y-%m')}-00T00:00:00Z/10"
    else:
        iso_date = f"+{dt.strftime('%Y-%m-%d')}T00:00:00Z/11"

    return iso_date


# Function to convert CSV to QuickStatements TSV
def csv_to_qs():
    
    # Define standard string fields
    STRING_FIELDS = [
        'Lit', 'Len', 'Lfr', 'Lde', 
        'Ait', 'Aen', 'Afr', 'Ade', 
        'Dit', 'Den', 'Dfr', 'Dde'
    ]
    
    SITELINK_FIELDS = [
        'itwiki', 'enwiki', 'frwiki', 'dewiki', 
        'commonswiki', 'itwikisource', 'enwikisource'
    ]
    
    # File selection dialog
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(title = "Seleziona file",filetypes= (("Tutti i file","*.*"),("CSV","*.csv")), multiple=False)
    
    if not file:
        print("Nessun file selezionato")
        return
    
    # Prepare output file
    filename = os.path.basename(file)
    filepath = os.path.dirname(file)
    new_file = os.path.join(filepath, f"{filename.split('.')[0]}_qs.tsv")

    # Read the input CSV file
    with open(file, 'r', encoding='utf-8') as f:
        with open(new_file, 'w', encoding='utf-8', newline='') as write_file:
        
            # Normalize BOM and read content
            content = f.read().lstrip('\ufeff')
            csv_file = io.StringIO(content)
            reader = csv.reader(csv_file)
            
            # Header mapping
            header_map = {}
            
            try:
                header = next(reader)
            except StopIteration:
                print("Impossible to read empty file")
                
            for idx, col_name in enumerate(header):
                
                name = col_name.strip()
                cell_type = None
                
                if name in STRING_FIELDS:
                    cell_type = 'string'
                elif name in SITELINK_FIELDS:
                    cell_type = 'sitelink'
                elif name.endswith('_STR'):
                    name = name[:-4]
                    cell_type = 'string'
                elif name.endswith('_NUM'):
                    name = name[:-4]
                    cell_type = 'number'
                elif name.endswith('_DATE'):
                    name = name[:-5]
                    cell_type = 'date'
                elif name.endswith('_GEO'):
                    name = name[:-4]
                    cell_type = 'coordinates'

                header_map[idx] = {'name': name, 'cell_type': cell_type}
            
            # Row processing
            for row in reader:
                
                # Skip empty rows
                if not any(row):
                    continue
                
                qid_value = None
                qs_commands = []
                
                # Process each cell in the row
                for column_index, cell in enumerate(row):
                    
                    if column_index not in header_map:
                        continue
                    
                    data = header_map[column_index]
                    col_name = data['name'].strip()
                    value = cell.strip()
                    
                    if not value:
                        continue

                    # Handle QID
                    if col_name.lower() == 'qid':
                        qid_value = value
                        continue
                    
                    prefix = qid_value if qid_value else 'LAST'
                    
                    formatted_value = value
                    
                    # Handle sitelinks
                    if data['cell_type'] == 'sitelink':
                        title = unquote(value)
                        if title.startswith('http://') or title.startswith('https://'):
                            title = title.split('/')[-1]
                        
                        title = title.replace('_', ' ')

                        qs_command = f'{prefix}|{col_name}:{title}'
                        qs_commands.append(qs_command)
                        continue 
                    
                    # Handle other columns
                    if data['cell_type'] == 'string':
                        formatted_value = f'"{value}"'
                    elif data['cell_type'] == 'date':
                        formatted_value = format_date(value) 
                        if not formatted_value: continue
                    elif data['cell_type'] == 'number':
                        formatted_value = value.replace(',', '.')
                    elif data['cell_type'] == 'coordinates':
                        formatted_value = f'@{value}'
                        
                    if not formatted_value:
                        continue

                    qs_command = f'{prefix}|{col_name}|{formatted_value}'
                    qs_commands.append(qs_command)

                # Write the processed row to the output file
                start_command = qid_value if qid_value else 'CREATE'
                
                write_file.write(f'{start_command}\n')
                
                for cmd in qs_commands:
                    write_file.write(f'{cmd}\n')
                    
                write_file.write('\n')
    
    print(f"File saved as {new_file}")
    
    # Open the output file with the default application
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', new_file))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(new_file)
    else:                                   # linux variants
        subprocess.call(('xdg-open', new_file))
    
    return


if __name__ == '__main__':
    try:
        csv_to_qs()
    except Exception as err:
        print(str(err))
        sys.exit()