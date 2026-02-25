import os
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from .metadata import collect_metadata

SUPPORTED_EXT = (
    ".png", ".jpg", ".jpeg", ".webp",
    ".mp4", ".mov", ".mkv", ".webm", ".avi"
)

CACHE_FILE = ".aiscan_cache.json"
CACHE_VERSION = 1

_cache_lock = Lock()


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


def load_cache(folder):

    path = os.path.join(folder, CACHE_FILE)

    if not os.path.exists(path):
        return {"version": CACHE_VERSION, "files": {}}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data.get("version") != CACHE_VERSION:
            return {"version": CACHE_VERSION, "files": {}}

        return data

    except Exception:
        return {"version": CACHE_VERSION, "files": {}}


def save_cache(folder, cache):

    path = os.path.join(folder, CACHE_FILE)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def scan(folder, threads=4, force=False, clear_cache=False):

    cache = load_cache(folder)

    if clear_cache:
        cache = {"version": CACHE_VERSION, "files": {}}

    results = []
    files = list(collect_files(folder))

    def process(path):

        stat = os.stat(path)
        mtime = stat.st_mtime
        size = stat.st_size

        if not force:
            entry = cache["files"].get(path)
            if entry:
                if entry["mtime"] == mtime and entry["size"] == size:
                    return {
                        "path": path,
                        **entry["result"]
                    }

        result = analyze(path)

        with _cache_lock:
            cache["files"][path] = {
                "mtime": mtime,
                "size": size,
                "result": {
                    "ai": result["ai"],
                    "tool": result["tool"],
                    "confidence": result["confidence"],
                }
            }

        return result

    with ThreadPoolExecutor(max_workers=threads) as ex:
        results = list(ex.map(process, files))

    save_cache(folder, cache)

    return results
