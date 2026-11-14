#!/usr/bin/env python3
"""news-image-01 entry program.

The entry image (entry.png — a one-page newspaper broadsheet summing up the
world news of Friday 13 November 2026, composed programmatically by
compose.py) is committed alongside this script. Running the program installs
it as the entry artifact in the output directory.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print(f"error: committed entry image is missing: {SOURCE}", file=sys.stderr)
        return 1
    size = os.path.getsize(SOURCE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    print(f"wrote {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
