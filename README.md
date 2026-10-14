# Dotfiles do Hyprland

Configuracoes do meu desktop Debian/Hyprland, organizadas como pacotes para o
[GNU Stow](https://www.gnu.org/software/stow/).

## Conteudo

- `hypr`: Hyprland em Lua, Hypridle, Hyprlock e scripts da sessao
- `waybar`: barra de status
- `kitty`: terminal
- `rofi`: launcher com cores do Pywal
- `wofi`: launcher de aplicativos com tema escuro e navegacao pelas setas
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
swww pywal python3 python3-pil jq btop fastfetch cava yazi tty-clock unimatrix
pipewire wireplumber nautilus google-chrome-stable
```

Tambem sao usadas as fontes JetBrains Mono, Symbols Nerd Font, FontAwesome,
Noto Sans e Noto Sans Mono CJK JP. O script `wal-palette.py` usa Pillow para
extrair as cores do wallpaper e Pywal para exportar a paleta. Imagens em tons
de cinza geram uma paleta monocromatica; imagens coloridas preservam seus tons
com ajustes de contraste para legibilidade.

## Instalacao

No Debian, instale primeiro o Stow:

```bash
sudo apt install stow
```

Clone o repositorio diretamente na sua pasta pessoal e crie os links:

```bash
git clone https://github.com/Mattaus-1/DebianM.git ~/dotfiles
cd ~/dotfiles
stow --target="$HOME" hypr waybar kitty rofi wofi swaync waypaper fastfetch local-bin
```

Se os caminhos de destino ja existirem como arquivos normais, faca backup e
remova-os antes de executar o Stow. Nao use `stow --adopt` sem revisar as
alteracoes, pois ele pode substituir o conteudo deste repositorio.

Para remover os links:

```bash
cd ~/dotfiles
stow --delete --target="$HOME" hypr waybar kitty rofi wofi swaync waypaper fastfetch local-bin
```

## Ajustes da maquina

Edite os monitores no inicio de `hypr/.config/hypr/hyprland.lua`. A configuracao
atual usa `DP-3` e `HDMI-A-1`, com dois workspaces em cada monitor.

`Super+Espaco` abre o Wofi. Use as setas para cima/baixo para selecionar um
aplicativo, Enter para abrir e Esc para fechar.

`Super+scroll`, em qualquer direcao, alterna entre os dois workspaces do
monitor em foco. O script de alternancia nao adiciona trava nem espera.

O Waypaper procura imagens em `~/Imagens`. Depois de escolher um wallpaper, os
scripts geram a paleta em `~/.cache/wal` e atualizam Waybar, Rofi, Kitty, SwayNC,
Cava e btop.

O Waypaper abre centralizado em uma janela flutuante de 900x650, sem blur nem
sombra. As cores das instancias abertas do Kitty sao atualizadas pelos sockets
`/tmp/kitty-socket-*` usando `kitty-palette-sync.sh`.

Firefox, Zed, Spotify, Obsidian, Nautilus, Chrome e o dashboard usam opacidade
total. O Hyprlock envia automaticamente a entrada ao atingir quatro caracteres;
ajuste ou remova `auto_submit_length` em `hyprlock.conf` conforme sua senha.

O atalho `Super+Ctrl+D` abre o dashboard opcional e requer Fastfetch, Yazi,
tty-clock, Unimatrix e Cava.
