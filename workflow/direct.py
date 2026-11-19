#!/usr/bin/python3
import os, sys, subprocess, json, re, plistlib
from pathlib import Path

def output(items):
    print(json.dumps({'items': items}))

q = os.environ.get('alfred_workflow_keyword', '') + ''.join(sys.argv[1:])
if not re.match(r'^[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)\s*[a-zA-Z°µμ]', q):
    output([])
    sys.exit()

source = None
for manifest in Path(__file__).resolve().parent.parent.glob('*/info.plist'):
    try:
        config = plistlib.loads(manifest.read_bytes())
        if config.get('bundleid') == 'com.alfredapp.vitor.unitconverter':
            source = manifest.parent
            break
    except (OSError, ValueError, plistlib.InvalidFileException):
        continue
if source is None or not (source / 'converter').is_file():
    output([{'title': 'Install the original Unit Converter workflow',
             'subtitle': 'Direct Search uses the Alfred Team Unit Converter engine.', 'valid': False}])
    sys.exit()

env = dict(os.environ)
for setting in config.get('userconfigurationconfig', []):
    spec = setting.get('config', {})
    value = spec.get('default', spec.get('defaultvalue', ''))
    env[setting['variable']] = str(int(value)) if isinstance(value, bool) else str(value)
preferences = source / 'prefs.plist'
if preferences.exists():
    for key, value in plistlib.loads(preferences.read_bytes()).get('variables', {}).items():
        env[key] = str(int(value)) if isinstance(value, bool) else str(value)
try:
    data = json.loads(subprocess.check_output([str(source / 'converter'), q], cwd=source, env=env, text=True, timeout=3))
    items = [i for i in data.get('items', []) if i.get('valid') and i.get('arg')]
    for item in items:
        item.pop('autocomplete', None)
        item['subtitle'] = item.get('subtitle', '') + ' — Return to copy'
    output(items)
except Exception:
    output([])
