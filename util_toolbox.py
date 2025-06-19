import sys
import logging
import ctypes
from pathlib import Path
from fontTools.ttLib import TTFont

logging.basicConfig(level=logging.DEBUG)

if hasattr(sys, 'frozen'):
    base = Path(sys._MEIPASS)
else:
    base = Path(sys.argv[0]).parent

filetypes = {
    'image': '.png',
    'icon': '.ico',
    'font': '.ttf',
}

themes = {
    'Dark': {
        'bg_color': '#000000',
        'ui_color': '#ffffff',
        'btn_color': '#828282',
        'btn_text': '#ffffff',
    },
    'Light': {
        'bg_color': '#ffffff',
        'ui_color': '#000000',
        'btn_color': '#4a4a4a',
        'btn_text': '#ffffff',
    }
}

extractroots = {
    "RobloxApp.zip": "",
    "redist.zip": "",
    "shaders.zip": "shaders/",
    "ssl.zip": "ssl/",

    "WebView2.zip": "",
    "WebView2RuntimeInstaller.zip": "WebView2RuntimeInstaller/",

    "content-avatar.zip": "content/avatar/",
    "content-configs.zip": "content/configs/",
    "content-fonts.zip": "content/fonts/",
    "content-sky.zip": "content/sky/",
    "content-sounds.zip": "content/sounds/",
    "content-textures2.zip": "content/textures/",
    "content-models.zip": "content/models/",

    "content-platform-fonts.zip": "PlatformContent/pc/fonts/",
    "content-platform-dictionaries.zip": "PlatformContent/pc/shared_compression_dictionaries/",
    "content-terrain.zip": "PlatformContent/pc/terrain/",
    "content-textures3.zip": "PlatformContent/pc/textures/",

    "extracontent-luapackages.zip": "ExtraContent/LuaPackages/",
    "extracontent-translations.zip": "ExtraContent/translations/",
    "extracontent-models.zip": "ExtraContent/models/",
    "extracontent-textures.zip": "ExtraContent/textures/",
    "extracontent-places.zip": "ExtraContent/places/"
}

def parse(filepath):
    config = {}
    try:
        with open(filepath,'r') as f:
            for line in f:
                line = line.strip()

                if not line or ' ' not in line:
                    continue

                key, value = line.split(' ', 1)
                config[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f'Could not find file: {filepath}')
    except Exception as e:
        raise Exception(e)
    return config

def write(filepath, config):
    existing = {}
    if Path(filepath).exists():
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ' ' not in line:
                    continue
                key, value = line.split(' ', 1)
                existing[key] = value

    existing.update(config)

    with open(filepath, 'w') as f:
        for key, value in existing.items():
            f.write(f'{key} {value}\n')

def uriparse(sequence):
    config = {}
    pairs = sequence.split('+')
    for pair in pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            config[key] = value
    return config

def getasset(name, type, assettheme='Light'):
    assetpath = base / 'assets' / type.lower()
    if type == 'icon' or type == 'image':
        assetpath = assetpath / assettheme.lower()
    if type == 'font':
        assetpath = base / 'assets' / 'ui' / 'fonts' / name.lower()
    if assetpath.exists():
        asset = name.lower() + filetypes.get(type, '')
        assetfile = assetpath / asset
        if assetfile.exists():
            logging.info(f'Asset {name} found! Path: {assetfile}')
            return str(assetfile)
        else:
            logging.error(f'Asset {name} not found. Path: {assetfile}')
    else:
        logging.error(f'Asset type {type} does not exist. Path: {assetpath}')

def setfont(fontname, fontsize): #i dont know if this the best way to do it but it works
    fontpath = getasset(fontname, 'font')
    ctypes.windll.gdi32.AddFontResourceExW(ctypes.c_wchar_p(fontpath), 0x10, 0)
    font = TTFont(fontpath)
    name = ''
    for record in font['name'].names:
        if record.nameID == 1:
            name = record.toUnicode()
            break
    return (name, fontsize)

configpath = Path(base / 'assets' / 'config' / '.astra')

def cleanup():
    logging.info(f'Application {sys.argv[0]} closed, cleaning up')
    fontname = parse(configpath).get('Font', 'inter')
    fontpath = getasset(fontname, 'font')
    ctypes.windll.gdi32.RemoveFontResourceW(fontpath)
    logging.info(f'Removed font {fontname} from memory')

    logging.info('Done, closing')
    sys.exit()

def centerwindow(win, width, height):
    win.update_idletasks()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    win.geometry(f"{width}x{height}+{x}+{y}")