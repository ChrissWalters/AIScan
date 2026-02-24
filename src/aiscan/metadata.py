from PIL import Image
from PIL.PngImagePlugin import PngImageFile
import piexif


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


def collect_metadata(path):
    meta = read_exif_metadata(path)
    if path.lower().endswith(".png"):
        meta += read_png_metadata(path)
    return meta
