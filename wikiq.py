from csv import reader, writer
import tkinter as tk
from tkinter import filedialog
import webbrowser
import subprocess, os, platform, sys


def main():
    
    file = filedialog.askopenfilename(title = "Seleziona file",filetypes= (("Tutti i file","*.*"),("CSV","*.csv")), multiple=False)
    filename = os.path.basename(file)
    filepath = os.path.dirname(file)
    new_file = os.path.join(filepath, filename.split('.')[0] + '_updated.csv')

    with open(file, 'r', encoding='utf-8') as csv_file:
        with open(new_file, 'w+', encoding='utf-8', newline='') as write_file:

            scriba = writer(write_file)

            for row in reader(csv_file):
                line = []
                for column in row:
                    if str(column) == 'qid':
                        scriba.writerow(row)
                        break 
                    elif str(column) == '':
                        line.append('')
                    else:
                        if not column.startswith('Q'):
                            column = '"' + str(column) + '"'
                            line.append(str(column))
                        else:
                            line.append(str(column))
                    
                if str(column) != 'qid':
                    scriba.writerow(line)

    out_filename = os.path.basename(new_file)
    txt_file = os.path.join(filepath, out_filename.split('.')[0] + '.txt')
    os.rename(new_file, txt_file)

    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', txt_file))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(txt_file)
    else:                                   # linux variants
        subprocess.call(('xdg-open', txt_file))
        
    return


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(str(err))
        sys.exit()
