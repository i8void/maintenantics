#!/usr/bin/env bash
# Render every Mermaid source in figures/mermaid/*.mmd to a PNG in figures/.
# Requires @mermaid-js/mermaid-cli (mmdc) and a Chromium available to Puppeteer.
#
#   npm install -g @mermaid-js/mermaid-cli
#   ./figures/render_mermaid.sh
#
# Flags: white background, scale 3 for crisp raster output.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
for src in "$here"/mermaid/*.mmd; do
  name="$(basename "${src%.mmd}")"
  echo "rendering $name"
  mmdc -i "$src" -o "$here/$name.png" -b white -s 3
done
echo "done"
