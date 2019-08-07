#!/usr/bin/env sh

pandoc -t markdown_strict --filter=pandoc-crossref --filter=pandoc-citeproc --standalone README.txt  -o README.md
