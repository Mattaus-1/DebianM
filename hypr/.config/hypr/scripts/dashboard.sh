#!/usr/bin/env bash
set -e
export PATH="$HOME/.local/bin:$PATH"
# An explicit shortcut keeps dashboard windows out of ongoing work at login.
if hyprctl clients -j | jq -e '.[] | select(.class == "iridescent-dashboard")' >/dev/null; then
  hyprctl dispatch workspace 1
  exit 0
fi
hyprctl dispatch workspace 1
kitty --class iridescent-dashboard --title Fastfetch -e bash -c 'fastfetch -c "$HOME/.config/fastfetch/dashboard.jsonc"; exec bash --norc' &
sleep 0.8
hyprctl dispatch layoutmsg preselect r
kitty --class iridescent-dashboard --title Yazi -e yazi &
sleep 0.8
hyprctl dispatch layoutmsg preselect d
kitty --class iridescent-dashboard --title Relógio -e tty-clock -t -C 6 -S -D -c &
sleep 0.8
hyprctl dispatch layoutmsg preselect d
kitty --class iridescent-dashboard --title Unimatrix -e unimatrix -s 90 -l k &
sleep 0.8
hyprctl dispatch layoutmsg preselect d
kitty --class iridescent-dashboard --title Cava -e cava -p "$HOME/.config/cava/iridescent.conf" &
