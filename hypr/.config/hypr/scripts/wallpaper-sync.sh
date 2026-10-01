#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
wallpaper=${1:?Escolha uma imagem}
test -f "$wallpaper"
mkdir -p "$HOME/.cache/wal" "$HOME/.local/state"
exec 9>"$HOME/.cache/wal/iridescent.lock"
flock 9
swww img "$wallpaper" --transition-type fade --transition-duration 1
printf '%s\n' "$wallpaper" > "$HOME/.local/state/wallpaper-current"
wal -i "$wallpaper" --backend modern_colorthief --contrast 3 -n -q -t -e
ln -sfn "$wallpaper" "$HOME/.cache/wal/current_wallpaper"
python3 "$HOME/.config/hypr/scripts/sync-palette.py"
bash "$HOME/.config/hypr/scripts/btop-pywal-theme.sh"
if pgrep -u "$UID" -x waybar >/dev/null; then pkill -u "$UID" -USR2 -x waybar; fi
if pgrep -u "$UID" -x swaync >/dev/null; then timeout 3 swaync-client -rs >/dev/null 2>&1 || true; fi
