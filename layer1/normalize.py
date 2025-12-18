import os
import shutil
import zipfile
import hashlib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

ARTIFACT_ROOT = os.path.join(PROJECT_ROOT, "artifacts")

def artifact_id_from_path(path: str) -> str:
    h = hashlib.sha256()
    h.update(os.path.abspath(path).encode())
    return h.hexdigest()[:16]

def create_artifact_dir(artifact_id: str) -> str:
    path = os.path.join(ARTIFACT_ROOT, artifact_id)
    os.makedirs(path, exist_ok=True)
    return path

def normalize_single_file(src: str, dest: str):
    shutil.copy2(src, os.path.join(dest, os.path.basename(src)))

def normalize_directory(src: str, dest: str):
    shutil.copytree(src, dest, dirs_exist_ok=True)

def normalize_zip(src: str, dest: str):
    with zipfile.ZipFile(src, "r") as z:
        z.extractall(dest)
