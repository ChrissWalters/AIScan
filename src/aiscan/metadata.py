from PIL import Image
from PIL.PngImagePlugin import PngImageFile
import piexif
import subprocess
import json


def read_png_metadata(path):
    data = ""
    try:
        img = Image.open(path)
        if isinstance(img, PngImageFile):
            for k, v in img.info.items():
                data += f"{k}:{v}\n"
    except Exception:
        pass
    return data


def read_exif_metadata(path):
    data = ""
    try:
        exif_dict = piexif.load(path)
        for ifd in exif_dict:
            if isinstance(exif_dict[ifd], dict):
                for tag in exif_dict[ifd]:
                    val = exif_dict[ifd][tag]
                    if isinstance(val, bytes):
                        val = val.decode(errors="ignore")
                    data += str(val) + "\n"
    except Exception:
        pass
    return data


def read_video_metadata(path):
    """
    Extract metadata from video containers using ffprobe.
    Requires ffmpeg/ffprobe installed on system.
    """
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            path,
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            return ""

        parsed = json.loads(result.stdout)

        data = ""

        # Container-level metadata
        if "format" in parsed and "tags" in parsed["format"]:
            for k, v in parsed["format"]["tags"].items():
                data += f"{k}:{v}\n"

        # Stream-level metadata
        for stream in parsed.get("streams", []):
            if "tags" in stream:
                for k, v in stream["tags"].items():
                    data += f"{k}:{v}\n"

        return data

    except Exception:
        return ""


def collect_metadata(path):
    meta = ""

    # Images
    meta += read_exif_metadata(path)

    if path.lower().endswith(".png"):
        meta += read_png_metadata(path)

    # Videos
    if path.lower().endswith((
        ".mp4", ".mov", ".mkv", ".webm", ".avi"
    )):
        meta += read_video_metadata(path)

    return meta
