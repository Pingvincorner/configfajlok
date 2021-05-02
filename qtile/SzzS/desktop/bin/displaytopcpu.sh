#!/bin/bash

#CPU
#ps -eo comm=Folyamat,%cpu=Százalék  --sort -%cpu | head --lines=10

TITLE=$(echo -e "\U0001f321 CPU zabálók")
MSG="$(ps -eo comm=Folyamat,%cpu=Százalék  --sort -%cpu | head --lines=10)"

dunstify "$TITLE" "$MSG" -u normal -t 10000 -i /usr/share/pixmaps/archlinux-logo.png -r 19700730
