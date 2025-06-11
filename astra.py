import customtkinter as tk
from pathlib import Path
from utils import parse, themes, uriparse
from customtkinter import set_appearance_mode
import sys
import darkdetect
import logging

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) > 1:
    uri = sys.argv[1]
    
    if uri == '--config'.lower():
        logging.info('add logic later')

if hasattr(sys, 'frozen'):
    base = Path(sys._MEIPASS)
else:
    base = Path(sys.argv[0]).parent

config = parse(base / 'assets' / 'config' / '.astra')
theme = config.get('Theme', 'Light')
version = config.get('Version', 'x.x.x')
mode = config.get('Mode', 'Frozen')

if theme == 'System':
    if darkdetect.isDark():
        theme = 'Dark'
    else:
        theme = 'Light'

main = tk.CTk()
main.geometry("400x150")
main.title(f'Astra {version}')

set_appearance_mode(theme)
main.configure(bg_color=themes[theme]['bg_color'])

print(theme)
main.mainloop()