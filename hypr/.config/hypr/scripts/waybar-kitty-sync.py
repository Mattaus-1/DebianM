#!/usr/bin/env python3
"""Synchronize Waybar palette with Kitty and CAVA."""
import fcntl
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

home = Path.home()
cache = home / '.cache/wal'
lock_file = cache / 'iridescent.lock'
palette_file = cache / 'colors-waybar.css'
style_file = home / '.config/waybar/style.css'
kitty_file = cache / 'colors-kitty-waybar.conf'
cava_file = home / '.config/cava/config'
pattern = re.compile(r'@define-color\s+([\w-]+)\s+(#[0-9a-fA-F]{3,8}|@[\w-]+)\s*;')


def atomic_write(path, content):
    if path.exists() and path.read_text() == content:
        return False
    fd, name = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent, text=True)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(content)
        os.chmod(name, path.stat().st_mode & 0o777 if path.exists() else 0o644)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return True


def sync():
    colors = {}
    for path in (palette_file, style_file):
        if path.exists():
            for name, value in pattern.findall(path.read_text()):
                colors[name] = value

    def resolve(name, seen=None):
        seen = seen or set()
        value = colors.get(name)
        if not value or name in seen:
            return None
        return resolve(value[1:], seen | {name}) if value.startswith('@') else value

    required = ['foreground', 'background'] + [f'color{i}' for i in range(16)]
    if not all(resolve(name) for name in required):
        raise SystemExit('Waybar palette is incomplete; keeping the previous colors')
    roles = {
        'cursor_text_color': 'background',
        'selection_foreground': 'background',
        'selection_background': 'color4',
        'url_color': 'color4',
        'active_border_color': 'color4',
        'inactive_border_color': 'color8',
        'bell_border_color': 'color1',
        'active_tab_foreground': 'background',
        'active_tab_background': 'color4',
        'inactive_tab_foreground': 'foreground',
        'inactive_tab_background': 'background',
        'tab_bar_background': 'background',
    }
    lines = [f'{name} {resolve(name)}' for name in ['foreground', 'background', 'cursor', *[f'color{i}' for i in range(16)]] if resolve(name)]
    lines += [f'{name} {resolve(source)}' for name, source in roles.items() if resolve(source)]
    atomic_write(kitty_file, '# Colors mirrored from Waybar\n' + '\n'.join(lines) + '\n')

    def rgb(value):
        digits = value.lstrip('#')
        if len(digits) in (3, 4):
            digits = ''.join(ch * 2 for ch in digits)
        return '#' + digits[:6]

    bar_colors = [rgb(resolve(name)) for name in ('color1', 'color4', 'color7')]
    cava_file.parent.mkdir(parents=True, exist_ok=True)
    template = cava_file.with_name('config.example')
    if cava_file.exists():
        original = cava_file.read_text()
    elif template.exists():
        original = template.read_text()
    else:
        original = '[general]\nframerate = 60\n\n[output]\nmethod = noncurses\n'
    block = ('[color]\nbackground = default\ngradient = 1\ngradient_count = 3\n'
             + ''.join(f"gradient_color_{i} = '{color}'\n" for i, color in enumerate(bar_colors, 1)))
    section = re.compile(r'^\[color\]\n.*?(?=^\[|\Z)', re.MULTILINE | re.DOTALL)
    updated = section.sub(lambda _: block + '\n', original, count=1) if section.search(original) else original + '\n' + block
    if atomic_write(cava_file, updated):
        result = subprocess.run(['pgrep', '-u', str(os.getuid()), '-x', 'cava'], capture_output=True, text=True, check=False)
        for pid in result.stdout.splitlines():
            try:
                os.kill(int(pid), signal.SIGUSR2)
            except (ProcessLookupError, PermissionError):
                pass

    for socket in Path('/tmp').glob('kitty-socket-*'):
        if socket.is_socket() and socket.stat().st_uid == os.getuid():
            subprocess.run(['kitty', '@', '--to', f'unix:{socket}', 'set-colors', '--all', '--configured', str(kitty_file)], timeout=3, check=False)
    subprocess.run(['pkill', '-u', str(os.getuid()), '-USR2', '-x', 'waybar'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    cache.mkdir(parents=True, exist_ok=True)
    if '--already-locked' in sys.argv:
        sync()
    else:
        with lock_file.open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            sync()
