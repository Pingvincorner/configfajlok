#!/bin/bash
xset -dpms s off
xrandr -s 3440x1440
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
numlockx on
picom -b
dunst &
nitrogen --restore &
volumeicon &
clipit &
#megasync &
#keepassxc &

