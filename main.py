#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261117.

The front page is pre-rendered by render.py into entry.png (standard
library only here, as the sandbox provides no PIL). This program copies
that image to the output directory the harness expects.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote", DST)
