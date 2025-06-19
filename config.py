import customtkinter as tk
import tkinter as ntk
from util_toolbox import parse, themes, getasset, base, setfont, cleanup, write, configpath, centerwindow
from customtkinter import set_appearance_mode
from PIL import Image

def config():

    main = tk.CTk()

    centerwindow(main, 600, 300)
    main.title('Configure Astra')

    config = parse(configpath)
    theme = config.get('Theme', 'Light')
    version = config.get('Version', 'x.x.x')
    font = config.get('Font', 'Inter')

    realtheme = theme

    globalfont = setfont(font,15)
    globalbig = setfont(font,24)
    globalmedium = setfont(font,18)
    globalsmall = setfont(font,12)

    if theme == 'System':
        import darkdetect
        if darkdetect.isDark():
            theme = 'Dark'
        else:
            theme = 'Light'

    set_appearance_mode(theme)
    main.configure(bg_color=themes[theme]['bg_color'])
    main.iconbitmap(getasset('logo', 'icon', theme))

    falsebg = ntk.Frame(master=main, background=themes[theme]['bg_color'])
    falsebg.pack(expand=True, fill='both')

    tabview = tk.CTkTabview(master=falsebg, fg_color=themes[theme]['bg_color'], bg_color=themes[theme]['bg_color'], corner_radius=14, segmented_button_selected_color='#538fd8', segmented_button_unselected_hover_color='#215da6', segmented_button_selected_hover_color='#215da6')
    tabview.pack(expand=True, fill='both', padx=10, pady=10)

    general = tabview.add('General')
    appearance = tabview.add('Appearance')
    about = tabview.add('About')

    # general tab
    
    #appearance tab
    
    themebox = tk.CTkComboBox(appearance, values=['Light', 'Dark', 'System'], font=globalfont, corner_radius=16, state='readonly', command=lambda value: write(configpath, {'Theme': value}))
    themebox.set(realtheme)
    themebox.pack(anchor='w')
    themebox_text = tk.CTkLabel(appearance, text='Theme', font=globalfont, bg_color=themes[theme]['bg_color'], text_color=themes[theme]['ui_color'], justify='center')
    themebox_text.pack(padx=35, anchor='w')

    # about tab
    logoimage = Image.open(getasset('logo', 'image', theme))
    logolabel = tk.CTkLabel(about, text='', image=tk.CTkImage(logoimage, size=(100, 100) if theme == 'Dark' else (85, 85)), bg_color=themes[theme]['bg_color'])
    logolabel.place(x=-5 if theme == 'Dark' else 10)

    logotext = tk.CTkLabel(about, text=f'Astra\n{version}',text_color=themes[theme]['ui_color'], font=globalbig, bg_color=themes[theme]['bg_color'],justify='center')
    logotext.place(x=10,y=100)

    infotext = tk.CTkLabel(about, text='A Roblox bootstrapper', font=globalmedium)
    infotext.place(x=100, y=10)

    infotext2 = tk.CTkLabel(about, text='and indirectly, others', font=globalsmall)
    infotext2.place(x=100, y=60)

    infotext3 = tk.CTkLabel(about, text='By itstheguy4873', font=globalmedium)
    infotext3.place(x=100, y=40)

    infotext4 = tk.CTkLabel(about, text=f'Running at {__file__}', font=globalfont)
    infotext4.place(x=100, y=100)

    main.mainloop()

    cleanup()

if __name__ == '__main__': #dont delete this
    config()