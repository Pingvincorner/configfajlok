#!/bin/bash
setxkbmap hu &
xdb -merge ~/.Xresources &
xset -dpms s off &
numlockx on &
picom -b
dunst &
nitrogen --restore &
clipit &
volumeicon &
