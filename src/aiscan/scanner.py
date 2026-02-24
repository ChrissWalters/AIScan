import os
import hashlib
from concurrent.futures import ThreadPoolExecutor
from .metadata import collect_metadata

SUPPORTED_EXT = (".png", ".jpg", ".jpeg", ".webp")


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def detect_ai(metadata):

    text = metadata.lower()

    if "steps:" in text and "sampler:" in text:
        return True, "automatic1111", 0.95

    if '"nodes"' in text and '"links"' in text:
        return True, "comfyui", 0.99

    if "invokeai" in text:
        return True, "invokeai", 0.8

    return False, "-", 0.0


def analyze(path):

    metadata = collect_metadata(path)
    ai, tool, conf = detect_ai(metadata)

    return {
        "path": path,
        "ai": ai,
        "tool": tool,
        "confidence": conf,
    }


def collect_files(root):
    for r, _, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith(SUPPORTED_EXT):
                yield os.path.join(r, f)


def scan(folder, threads=4):

    files = list(collect_files(folder))

    with ThreadPoolExecutor(max_workers=threads) as ex:
        results = list(ex.map(analyze, files))

    return results
