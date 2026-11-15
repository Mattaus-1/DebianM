#!/usr/bin/env bash
set -euo pipefail
lock="${XDG_RUNTIME_DIR:-/tmp}/waybar-btop.lock"
exec 9>"$lock"
if flock -n 9; then
    kitty --class waybar-btop --title btop btop
else
    for _ in {1..10}; do
        if hyprctl clients -j | jq -e '.[] | select(.class == "waybar-btop")' >/dev/null; then
            hyprctl eval 'hl.dispatch(hl.dsp.focus({ window = "class:waybar-btop" }))' >/dev/null
            exit 0
        fi
        sleep 0.1
    done
fi
