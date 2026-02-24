import argparse
import json
from datetime import datetime
from .scanner import scan


def main():

    parser = argparse.ArgumentParser(
        description="AI Image Workflow Scanner"
    )
    parser.add_argument("folder")
    args = parser.parse_args()

    results = scan(args.folder)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"aiscan_{ts}.txt"

    with open(outfile, "w", encoding="utf-8") as f:
        for r in results:
            line = f"{r['path']} | {'yes' if r['ai'] else 'no'} | {r['tool']}"
            f.write(line + "\n")

    print("Output:", outfile)
