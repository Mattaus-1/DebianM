#!/bin/sh

workspace_id=$(hyprctl activeworkspace -j | jq -r '.id')

case "$workspace_id" in
    1|3) hyprctl dispatch "hl.dsp.focus({workspace='r~2'})" ;;
    2|4) hyprctl dispatch "hl.dsp.focus({workspace='r~1'})" ;;
esac
