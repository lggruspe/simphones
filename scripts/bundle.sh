#!/usr/bin/env bash

# Bundle CSV, README and LICENSE files.

ra="$(pwd)"
temp="$(mktemp -d)"
path="$temp/simphones-0.1.0"
mkdir -p "$path"
cp README.md simphones.csv "$path"
cp LICENSES/CC_BY-SA_3.0.txt "$path/LICENSE.txt"
cd "$temp" || exit 1
tar -czvf simphones-0.1.0.tar.gz simphones-0.1.0
mv simphones-0.1.0.tar.gz "$ra"
cd "$ra" || exit 1
rm -rf "$temp"
