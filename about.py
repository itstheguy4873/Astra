import customtkinter as tk
from customtkinter import set_appearance_mode
from utils import parse, themes
from pathlib import Path
from PIL import Image
import darkdetect
import sys

if hasattr(sys, 'frozen'):
    base = Path(sys._MEIPASS)
else:
    base = Path(sys.argv[0]).parent

config = parse(base / 'assets' / 'config' / '.astra')
theme = config.get('Theme', 'Light')
version = config.get('Version', 'x.x.x')

if theme == 'System':
    if darkdetect.isDark():
        theme = 'Dark'
    else:
        theme = 'Light'

main = tk.CTk()
main.geometry("500x300")
main.title("About Astra")

set_appearance_mode(theme)
main.configure(bg_color=themes[theme]['bg_color'])

logopath = base / 'assets' / 'images' / theme.lower() / 'logo.png'
logoimage = Image.open(logopath)
logolabel = tk.CTkLabel(main, image=tk.CTkImage(logoimage, size=(100,100)), text="")
logolabel.pack(pady=20)

logotext = tk.CTkLabel(main, text=f'Astra {version}', font=('Arial', 20, 'bold'), text_color=themes[theme]['ui_color'])
logotext.pack(pady=10)
main.mainloop()