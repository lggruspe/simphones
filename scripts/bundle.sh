#!/usr/bin/env bash

# Bundle CSV, README and LICENSE files.

version="0.1.1"
ra="$(pwd)"
temp="$(mktemp -d)"
path="$temp/simphones-$version"
mkdir -p "$path"
cp README.md simphones.csv "$path"
cp LICENSES/CC_BY-SA_3.0.txt "$path/LICENSE.txt"
cd "$temp" || exit 1
tar -czvf "simphones-$version.tar.gz" "simphones-$version"
mv "simphones-$version.tar.gz" "$ra"
cd "$ra" || exit 1
rm -rf "$temp"
