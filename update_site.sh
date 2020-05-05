#!/bin/bash

#Portugal data update
python covid19_pt.py
echo "***   Portugal data updated  ***"

#WORLD data update
sshpass -p 'rp!1128' scp covid_19_clean_complete.csv pi@rpi4b:/var/www/html/
python covid19_world.py
echo "***  world data updated   ***"

#upload to the pi Web server
sshpass -p 'rp!1128' scp *.png pi@rpi4b:/var/www/html/
echo "***   uploaded to the pi Web server   ***"

