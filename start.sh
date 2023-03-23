#!/bin/bash

# configure the bot
python3 -m simplebot init deltahelp@disroot.org Francy82+
python3 -m simplebot -a deltahelp@disroot.org set_name SwissBot
python3 -m simplebot -a deltahelp@disroot.org set_avatar bot.jpeg
# buscador y subtítulos 
python3 -m simplebot -a deltahelp@disroot.org plugin --add ./url.py
# tira los dados 
python3 -m simplebot -a deltahelp@disroot.org plugin --add ./dice.py
#File to Link
python3 -m simplebot -a deltahelp@disroot.org plugin --add ./up.py


# add admin plugin
   # python3 -m simplebot -a deltahelp@disroot.org plugin --add ./admin.py
    python3 -m simplebot -a deltahelp@disroot.org admin --add frankramiro.martinez@nauta.cu

# start the bot
python3 -m simplebot -a deltahelp@disroot.org serve
