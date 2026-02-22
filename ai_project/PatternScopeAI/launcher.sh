#!/bin/bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
RESOURCES="$DIR/../Resources"
exec "$DIR/PatternVision.bin" -devResPath="$RESOURCES" "$@"
