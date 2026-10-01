# Dotfiles do Hyprland

Configuracoes do meu desktop Debian/Hyprland, organizadas como pacotes para o
[GNU Stow](https://www.gnu.org/software/stow/).

## Conteudo

- `hypr`: Hyprland em Lua, Hypridle, Hyprlock e scripts da sessao
- `waybar`: barra de status
- `kitty`: terminal
- `rofi`: launcher com cores do Pywal
- `swaync`: central de notificacoes
- `waypaper`: seletor de wallpapers
- `fastfetch`: configuracao usada pelo dashboard
- `local-bin`: comandos auxiliares para bloqueio e wallpaper

Caches, estado local, binarios e wallpapers nao sao versionados. A tela de
bloqueio usa uma captura da tela para nao depender de uma imagem privada.

## Requisitos

Este setup usa uma versao do Hyprland com a API Lua global `hl`. Uma instalacao
padrao que aceite apenas `hyprland.conf` nao carregara `hyprland.lua`.

Dependencias principais:

```text
hyprland hypridle hyprlock waybar swaync kitty rofi wofi waypaper
swww pywal python3 jq btop fastfetch cava yazi tty-clock unimatrix
pipewire wireplumber nautilus google-chrome-stable
```

Tambem sao usadas as fontes JetBrains Mono, Symbols Nerd Font, FontAwesome,
Noto Sans e Noto Sans Mono CJK JP. O script de cores espera o backend
`modern_colorthief` do Pywal.

## Instalacao

No Debian, instale primeiro o Stow:

```bash
sudo apt install stow
```

Clone o repositorio diretamente na sua pasta pessoal e crie os links:

```bash
git clone URL_DO_REPOSITORIO ~/dotfiles
cd ~/dotfiles
stow --target="$HOME" hypr waybar kitty rofi swaync waypaper fastfetch local-bin
```

Se os caminhos de destino ja existirem como arquivos normais, faca backup e
remova-os antes de executar o Stow. Nao use `stow --adopt` sem revisar as
alteracoes, pois ele pode substituir o conteudo deste repositorio.

Para remover os links:

```bash
cd ~/dotfiles
stow --delete --target="$HOME" hypr waybar kitty rofi swaync waypaper fastfetch local-bin
```

## Ajustes da maquina

Edite os monitores no inicio de `hypr/.config/hypr/hyprland.lua`. A configuracao
atual usa `DP-3` e `HDMI-A-1`, com dois workspaces em cada monitor.

O Waypaper procura imagens em `~/Imagens`. Depois de escolher um wallpaper, os
scripts geram a paleta em `~/.cache/wal` e atualizam Waybar, Rofi, Kitty, SwayNC,
Cava e btop.

O atalho `Super+Ctrl+D` abre o dashboard opcional e requer Fastfetch, Yazi,
tty-clock, Unimatrix e Cava.
