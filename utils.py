import os

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
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ' ' not in line:
                    continue
                key, value = line.split(' ', 1)
                existing[key] = value
    existing.update(config)

    try:
        with open(filepath, 'w') as f:
            for key, value in existing.items():
                f.write(f'{key} {value}\n')
    except Exception as e:
        print(e)

def uriparse(sequence):
    config = {}
    pairs = sequence.split('+')
    for pair in pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            config[key] = value
    return config

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
    
