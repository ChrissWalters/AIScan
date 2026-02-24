# AIScan – AI Image Workflow Scanner

*AIScan* is a platform-independent Python tool that recursively scans images in a folder and outputs whether they were created by AI generators. It supports popular AI tools such as *Automatic1111*, *ComfyUI*, and *InvokeAI*. Results are output to a *TXT file*.
---

## Features

- Recursive folder search
- Supports PNG, JPG/JPEG, and WEBP
- AI workflow detection:
  - Automatic1111
  - ComfyUI (including workflow JSON)
  - InvokeAI
- Output:
  - TXT file: `Path | AI Gen yes/no | Recognized tool`
- Cross-platform: Linux, Windows, macOS
- Fast scanning through threading
- Hash cache for repeated scans

---

## Installation

### 1. clone repository

```bash
git clone https://github.com/deinusername/aiscan.git
cd aiscan
```

### 2. create virtual envirmoment

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Windows (CMD)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. install dependencies

```bash
pip install .
```

---

## usage

After installation, the CLI command `aiscan` is available.

### basic command

```bash
aiscan <Ordner>
```

Beispiel:

```bash
aiscan ~/Bilder
```

The results are automatically saved in a TXT file in the project folder, e.g.:

```
aiscan_20260224_153000.txt
```

### uutput format (TXT)

```
Path/to/file | yes/no | used AI-Tool
```

example:

```
/home/user/Bilder/a.png | yes | automatic1111
/home/user/Bilder/b.png | yes | comfyui
/home/user/Bilder/photo.jpg | no | -
```

---

## cross-platform notes

| platform | (re-)activate venv |
|-----------|--------------------|
| Linux/macOS | `source .venv/bin/activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows CMD | `.venv\Scripts\activate.bat` |

Disabling the virtual environment:

```bash
deactivate
```

---

## Entwicklerhinweise

- modular design:
  - `metadata.py` - Metadata extraction
  - `scanner.py` - AI-detection & threaded scan
  - `cli.py` - Entry Point / CLI
-  New AI tools can be added using the `detect_ai()` function in `scanner.py`..

---

## Lizenz

<a href="https://github.com/ChrissWalters/AIScan">AIScan</a> © 2026 by <a href="https://github.com/ChrissWalters/">https://github.com/ChrissWalters/</a> is licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">
