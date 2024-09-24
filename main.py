import glob
import tkinter as tk
from tkinter import filedialog
from create_index import create_index

def get_file_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # put dialog window on top of other windows
    root.lift()
    root.attributes('-topmost', True)
    root.after(1, lambda: root.focus_force())
    root.update() 

    file_path = filedialog.askdirectory(mustexist=True)  # Open file dialog

    # close tkinter window 
    root.destroy()
    return file_path


use_default_or_custom = input('Would you prefer to use the default (d) or custom (c) file path? > ')
if use_default_or_custom == 'd':
    all_files = glob.glob('/Users/spencer/Documents/email_papers_script/sample_pdfs/*.pdf')
elif use_default_or_custom == 'c':
    print('If a directory selection screen does not appear, check the task bar.')
    all_files = get_file_path()
else:
    print('Unrecognized input. Please try again with c or d.')
    exit(0)

ind = create_index(all_files)
print(ind)

