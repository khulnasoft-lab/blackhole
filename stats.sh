#!/usr/bin/env bash

# Exit on error, undefined variable, and pipefail
set -euo pipefail

# Output file
OUT_FILE="stats.out"

# Clear the output file and add a header
echo "Date,Entries" > "$OUT_FILE"

# Get tags sorted by creation date and process each
git tag --sort=creatordate --format='%(refname:short),%(creatordate:short)' | while IFS=',' read -r TAG DATE; do
  # Checkout just readmeData.json from the tag (no HEAD detachment)
  git checkout "tags/$TAG" -- readmeData.json 2>/dev/null || continue

  # Extract entries using jq, fallback to 0 on failure
  entries=$(jq -r '.base.entries // 0' readmeData.json 2>/dev/null || echo 0)

  # Output to file
  echo "$DATE,$entries" >> "$OUT_FILE"
done

# Optionally restore the file if needed (uncomment the below line)
# git checkout HEAD -- readmeData.json
