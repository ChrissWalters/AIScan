import argparse
from datetime import datetime
from .scanner import scan


def main():

    parser = argparse.ArgumentParser(
        description="AI Workflow Scanner (Images + Videos)"
    )

    parser.add_argument("folder")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--force", action="store_true",
                        help="Ignore cache and rescan all files")
    parser.add_argument("--clear-cache", action="store_true",
                        help="Delete cache before scanning")

    args = parser.parse_args()

    results = scan(
        args.folder,
        threads=args.threads,
        force=args.force,
        clear_cache=args.clear_cache,
    )

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"aiscan_{ts}.txt"

    with open(outfile, "w", encoding="utf-8") as f:
        for r in results:
            line = f"{r['path']} | {'yes' if r['ai'] else 'no'} | {r['tool']} | {r['confidence']}"
            f.write(line + "\n")

    print("Output:", outfile)
