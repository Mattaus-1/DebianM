#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess

home = Path.home()
palette = json.loads((home / '.cache/wal/colors.json').read_text())
colors = palette['colors']
# pywal 3 does not ship a Waybar template on every distribution.
css = '\n'.join(f'@define-color {k} {v};' for k, v in {**palette['special'], **colors}.items())
(home / '.cache/wal/colors-waybar.css').write_text(css + '\n')
accent = colors['color4'].lstrip('#')
subprocess.run(['hyprctl', 'eval', f"hl.config({{general={{col={{active_border='rgb({accent})'}}}}}})"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
cava = home / '.config/cava/iridescent.conf'
cava.write_text('[general]\nframerate = 60\nbars = 20\n[output]\nmethod = ncurses\n[color]\nbackground = default\ngradient = 1\ngradient_count = 2\ngradient_color_1 = "' + colors['color1'] + '"\ngradient_color_2 = "' + colors['color4'] + '"\n')
