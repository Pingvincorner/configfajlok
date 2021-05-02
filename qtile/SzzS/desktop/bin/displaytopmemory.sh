#!/bin/bash

#mem
#free -h --si| awk 'NR==2 { print $2 " totál, " $3 " használatban." }'
#ps -eo comm=Folyamat,%mem=Százalék  --sort -%mem | head --lines=10

T="$(free -h --si | awk 'NR==2 { print $2 " totál, " $3 " használatban." }')"
TITLE=$(echo -e "\U0001f9e0 $T")
MSG="$(ps -eo comm=Folyamat,%mem=Százalék  --sort -%mem | head --lines=10)"

dunstify "$TITLE" "$MSG" -u normal -t 10000 -i /usr/share/pixmaps/archlinux-logo.png -r 19700731
