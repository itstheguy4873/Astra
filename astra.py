import customtkinter as tk
import tkinter as ntk
from util_toolbox import parse, themes, getasset, base, setfont, cleanup
from customtkinter import set_appearance_mode
from PIL import Image
from config import config
import sys
import darkdetect
import logging

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) > 1:
    uri = sys.argv[1]
    
    if uri == '--config'.lower():
        config()

config = parse(base / 'assets' / 'config' / '.astra')
theme = config.get('Theme', 'Light')
version = config.get('Version', 'x.x.x')
font = config.get('Font', 'Inter')

globalfont = setfont(font,24)

if theme == 'System':
    if darkdetect.isDark():
        theme = 'Dark'
    else:
        theme = 'Light'

main = tk.CTk()
main.geometry("400x150")
main.title(f'Astra {version}')
main.resizable(False, False)

set_appearance_mode(theme)
main.configure(bg_color=themes[theme]['bg_color'])
main.iconbitmap(getasset('logo', 'icon', theme))

falsebg = ntk.Frame(master=main, background=themes[theme]['bg_color']) #i hate windows 11 with a fiery passion
falsebg.pack(expand=True, fill='both')

logoimage = Image.open(getasset('logo', 'image', theme))
logolabel = tk.CTkLabel(main, text='', image=tk.CTkImage(logoimage, size=(100, 100) if theme == 'Dark' else (85, 85)), bg_color=themes[theme]['bg_color']) #resize the images manually? NOPE
logolabel.place(x=210, y=20)

logotext = tk.CTkLabel(main, text=f'Astra\n{version}',text_color=themes[theme]['ui_color'], font=globalfont, bg_color=themes[theme]['bg_color'],justify='center')
logotext.place(x=320,y=35)

main.mainloop()

cleanup()