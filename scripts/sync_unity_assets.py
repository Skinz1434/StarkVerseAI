import os
import shutil
import subprocess
import json
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(REPO_DIR, '..'))
UNITY_PROJECT_PATH = r"C:\\Users\\skinn\\IronAydan"
UNITY_EXECUTABLE = r"C:\\Program Files\\Unity\\Hub\\Editor\\2020.3.0f1\\Editor\\Unity.exe"
SOURCE_DIR = os.path.join(PROJECT_ROOT, 'AI_Generated')
DEST_DIR = os.path.join(UNITY_PROJECT_PATH, 'Assets', 'AI_Generated')
LOG_FILE = os.path.join(PROJECT_ROOT, 'project_log.json')

# pull latest repo changes
subprocess.run(['git', 'pull', 'origin', 'main'], cwd=PROJECT_ROOT)

entries = []
if os.path.isdir(SOURCE_DIR):
    for root, _, files in os.walk(SOURCE_DIR):
        for fname in files:
            src_path = os.path.join(root, fname)
            rel_path = os.path.relpath(src_path, SOURCE_DIR)
            dest_path = os.path.join(DEST_DIR, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            timestamp = datetime.utcnow().isoformat() + 'Z'
            agent = 'unknown'
            if 'Prefabs' in rel_path:
                agent = 'StarkPackager AI'
            elif 'Scripts' in rel_path:
                agent = 'StarkLogic AI'
            elif 'Animations' in rel_path:
                agent = 'StarkMotion AI'
            elif 'Audio' in rel_path:
                agent = 'StarkSound AI'
            elif 'Metadata' in rel_path:
                agent = 'StarkAssets AI'
            entries.append(f"[{timestamp}] copied {rel_path} via {agent}")

if entries:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}
    log = data.get('log', [])
    log.extend(entries)
    data['log'] = log
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# trigger Unity to import assets
if os.path.isfile(UNITY_EXECUTABLE):
    subprocess.run([
        UNITY_EXECUTABLE,
        '-quit',
        '-batchmode',
        '-projectPath', UNITY_PROJECT_PATH,
        '-executeMethod', 'StarkverseImporter.SyncAssets'
    ])
else:
    print('Unity executable not found. Skipping import step.')
