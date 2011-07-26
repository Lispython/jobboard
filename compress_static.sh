#!/bin/bash          

echo "Static compressor"

COMPRESSOR_PATH="/usr/bin/yui-compressor"
STATIC_PATH="./static"
MEDIA_PATH="./media"

for f in `find "$STATIC_PATH" "$MEDIA_PATH"  \( -name '*.dev.js' -or -name '*.dev.css' \)`; do
	command="$COMPRESSOR_PATH --type ${f##*.} -o ${f%.*.*}.min.${f##*.} $f"
	echo $command
	$command
done