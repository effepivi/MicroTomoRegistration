#!/usr/bin/sh

pandoc -t markdown_strict --filter=pandoc-citeproc --filter=pandoc-crossref --standalone README.txt  -o README.md
