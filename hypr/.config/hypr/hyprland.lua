-- IridescentGlow/hyprland-dotfiles, adapted for Debian.
require('config/aesthetics')
require('config/windows')

local home = os.getenv('HOME')
local scripts = home .. '/.config/hypr/scripts/'
hl.monitor({output='DP-3', mode='1920x1080@60', position='0x0', scale=1})
hl.monitor({output='HDMI-A-1', mode='1920x1080@100', position='1920x0', scale=1})
for i=1,4 do
    hl.workspace_rule({workspace=tostring(i), monitor=i<=2 and 'DP-3' or 'HDMI-A-1', persistent=true, default=i==1 or i==3})
end
hl.config({
    input={kb_layout='us', follow_mouse=1, sensitivity=-0.4, touchpad={natural_scroll=true}},
    misc={disable_hyprland_logo=true, force_default_wallpaper=0, focus_on_activate=true},
})
local function exec(key, cmd) hl.bind(key, hl.dsp.exec_cmd(cmd)) end
exec('SUPER + Return', 'kitty --single-instance')
hl.bind('SUPER + Q', hl.dsp.window.close())
hl.bind('SUPER + V', hl.dsp.window.float({action='toggle'}))
exec('SUPER + F', 'hyprctl dispatch fullscreen')
hl.bind('SUPER + P', hl.dsp.window.pseudo())
hl.bind('SUPER + J', hl.dsp.layout('togglesplit'))
exec('SUPER + E', 'nautilus')
exec('SUPER + SPACE', 'wofi --show drun')
exec('SUPER + S', 'google-chrome-stable')
exec('SUPER + W', home .. '/.local/bin/wallpaper-picker')
exec('F3', home .. '/.local/bin/wallpaper-picker')
exec('SUPER + N', 'swaync-client -t')
exec('SUPER + L', home .. '/.local/bin/lock-screen')
exec('SUPER + M', 'hyprctl dispatch exit')
exec('SUPER + CTRL + D', 'bash ' .. scripts .. 'dashboard.sh')
for _,dir in ipairs({'left','right','up','down'}) do
    hl.bind('SUPER + ' .. dir, hl.dsp.focus({direction=dir}))
end
for i=1,2 do
    hl.bind('SUPER + ' .. i, hl.dsp.focus({workspace='r~' .. i}))
    hl.bind('SUPER + SHIFT + ' .. i, hl.dsp.window.move({workspace='r~' .. i}))
end
exec('SUPER + mouse_down', home .. '/.config/hypr/toggle-workspace.sh')
exec('SUPER + mouse_up', home .. '/.config/hypr/toggle-workspace.sh')
hl.bind('SUPER + mouse:272', hl.dsp.window.drag(), {mouse=true})
hl.bind('SUPER + mouse:273', hl.dsp.window.resize(), {mouse=true})
hl.bind('XF86AudioRaiseVolume', hl.dsp.exec_cmd('wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+'), {locked=true, repeating=true})
hl.bind('XF86AudioLowerVolume', hl.dsp.exec_cmd('wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-'), {locked=true, repeating=true})
hl.bind('XF86AudioMute', hl.dsp.exec_cmd('wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle'), {locked=true})
hl.bind('XF86AudioMicMute', hl.dsp.exec_cmd('wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle'), {locked=true})
hl.window_rule({name='yugioh-wine-desktop',match={class='^(explorer.exe)$',title='^(YuGiOh - Wine Desktop)$'},float=true,size='800 600',center=true})
hl.window_rule({name='dashboard',match={class='^(iridescent-dashboard)$'},opacity='0.85 0.75',workspace=1})
hl.window_rule({name='chrome-opacity',match={class='^(google-chrome)$'},opacity='0.95 0.90'})
hl.on('hyprland.start', function()
    hl.exec_cmd("sh -c 'pgrep -x swww-daemon >/dev/null || " .. home .. "/.local/bin/swww-daemon'")
    hl.exec_cmd('sh -c "sleep 2; ' .. home .. '/.local/bin/wallpaper-picker --restore"')
    hl.exec_cmd('hypridle')
    hl.exec_cmd('waybar')
    hl.exec_cmd('swaync')
end)
