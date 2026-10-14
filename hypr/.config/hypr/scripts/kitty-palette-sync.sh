#!/usr/bin/env bash
set -euo pipefail
palette="$HOME/.cache/wal/colors-kitty.conf"
test -r "$palette"
for socket in /tmp/kitty-socket-*; do
    [[ -S "$socket" && -O "$socket" ]] || continue
    if ! timeout 3 kitty @ --to "unix:$socket" set-colors --all --configured \
        "$palette"; then
        printf 'Não foi possível atualizar as cores do Kitty: %s\n' "$socket" >&2
    fi
done
