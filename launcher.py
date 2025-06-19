import customtkinter as tk
import tkinter as ntk
import requests
import os
import shutil
import logging
import zipfile
import io
import psutil
import pythoncom
import winreg as reg
import xml.etree.ElementTree as ET
from util_toolbox import themes, parse, configpath, cleanup, getasset, setfont, extractroots, centerwindow
from subprocess import Popen
from PIL import Image
from customtkinter import set_appearance_mode
from pathlib import Path
from win32com.shell import shell # type: ignore
from tkinter import messagebox as mb

def launch(mode='app'):
    try:
        config = parse(configpath)
        theme = config.get('Theme', 'Light')
        font = config.get('Font', 'Inter')
        appenabled = config.get('RobloxAppEnabled', 'Y')
        
        globalfont = setfont(font,15)

        main = tk.CTk()
        centerwindow(main, 400, 225)
        main.title('Astra')
        main.resizable(False, False)
        main.iconbitmap(getasset('logo', 'icon', theme))

        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == 'RobloxPlayerBeta.exe'.lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        falsebg = ntk.Frame(master=main, background=themes[theme]['bg_color'])
        falsebg.pack(expand=True, fill='both')

        logoimage = Image.open(getasset('logo', 'image', theme))
        logolabel = tk.CTkLabel(main, text='', image=tk.CTkImage(logoimage, size=(100, 100) if theme == 'Dark' else (85, 85)), bg_color=themes[theme]['bg_color'])
        logolabel.place(x=155,y=20)

        statustext = tk.CTkLabel(main, text='Status', font=globalfont, bg_color=themes[theme]['bg_color'], width=100)
        statustext.place(x=200,y=125, anchor='center')

        statuslabel = tk.CTkProgressBar(main, mode='indeterminate')
        statuslabel.place(x=100,y=175)
        statuslabel.start()

        set_appearance_mode(theme)
        main.configure(bg_color=themes[theme]['bg_color'])

        #this wasn't fun to code

        response = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer')
        if response.status_code == 200:
            data = response.json()
            rlatestver = data.get('clientVersionUpload', 'NotFound')
        else:
            mb.showerror('Error', 'Failed to fetch version information.')
            cleanup()

        fverurlbase = f'https://setup.rbxcdn.com/{rlatestver}-'

        rbxpath = Path(os.environ.get('LOCALAPPDATA')) / 'Roblox'
        
        for item in Path(rbxpath / 'Versions').iterdir():
            if item.is_dir():
                shutil.rmtree(item)

        main.update()

        installdir = rbxpath / 'Versions' / rlatestver
        installdir.mkdir(exist_ok=True)

        for key, value in extractroots.items():
            response = requests.get(f'{fverurlbase}{key}')
            if response.status_code == 200:
                zipbytes = io.BytesIO(response.content)
                main.after(0, lambda: statustext.configure(text=f'Extract {key}'))
                main.update()

                with zipfile.ZipFile(zipbytes) as zip_file:
                    zipdir = installdir / value
                    zipdir.mkdir(parents=True, exist_ok=True)

                    zip_file.extractall(zipdir)

        main.after(0, lambda: statustext.configure(text='Configure Registry'))
        key1 = reg.OpenKeyEx(reg.HKEY_CURRENT_USER, r'Software\ROBLOX Corporation\Environments\roblox-player', 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key1, 'clientExe', 0, reg.REG_SZ, str(installdir / 'RobloxPlayerLauncher.exe'))
        reg.SetValueEx(key1, 'version', 0, reg.REG_SZ, rlatestver)
        reg.SetValueEx(key1, None, 0, reg.REG_SZ, str(installdir / 'RobloxPlayerInstaller.exe'))
        if appenabled == 'Y':
            reg.SetValueEx(key1, 'LaunchExp', 0, reg.REG_SZ, 'InApp')
        else:
            reg.SetValueEx(key1, 'LaunchExp', 0, reg.REG_SZ, 'InBrowser')
        reg.CloseKey(key1)

        key2 = reg.OpenKeyEx(reg.HKEY_CURRENT_USER, r'Software\ROBLOX Corporation\Environments\roblox-player\Capabilities', 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key2, 'ApplicationIcon', 0, reg.REG_EXPAND_SZ, f'"{str(installdir / "RobloxPlayerBeta.exe")}",0')
        reg.CloseKey(key2)

        key3 = reg.OpenKeyEx(reg.HKEY_CLASSES_ROOT, r'roblox-player\shell\open\command', 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key3, 'version', 0, reg.REG_SZ, rlatestver)
        reg.SetValueEx(key3, None, 0, reg.REG_SZ, f'"{str(installdir / "RobloxPlayerBeta.exe")}" %1')
        reg.CloseKey(key3)

        logging.info('Successfully wrote registry')

        shelllink = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)

        shelllink.SetPath(str(installdir / 'RobloxPlayerLauncher.exe'))
        shelllink.SetArguments('roblox-player:1+launchmode:app')
        shelllink.SetWorkingDirectory(os.path.dirname(str(installdir / 'RobloxPlayerLauncher.exe')))
        shelllink.SetIconLocation(str(installdir / 'RobloxPlayerBeta.exe'), 0)

        persistfile = shelllink.QueryInterface(pythoncom.IID_IPersistFile)
        lnk = str(Path(os.environ.get('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Roblox' / 'Roblox Player.lnk')
        persistfile.Save(lnk, 0)

        appsettingsxml = installdir / 'AppSettings.xml'
        settingsxml = ET.Element('Settings')
        contentfolderxml = ET.SubElement(settingsxml, 'ContentFolder')
        contentfolderxml.text = 'content'
        baseurlxml = ET.SubElement(settingsxml, 'BaseUrl')
        baseurlxml.text = 'http://www.roblox.com'

        tree = ET.ElementTree(settingsxml)
        tree.write(appsettingsxml, encoding='utf-8', xml_declaration=False)

        if mode == 'app':
            proc = Popen([str(installdir / 'RobloxPlayerBeta.exe'), '--app'])
        else:
            proc = Popen([str(installdir / 'RobloxPlayerBeta.exe'), mode])

        main.withdraw()

        main.mainloop()

        cleanup()
    
    except Exception as e:
        mb.showerror('Astra', f'Astra encountered an error: {e}')


if __name__ == '__main__':
    launch('app')