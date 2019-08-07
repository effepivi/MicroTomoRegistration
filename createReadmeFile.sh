#!/usr/bin/sh

pandoc -t markdown_strict --filter=pandoc-citeproc --standalone README.txt  -o README.md
