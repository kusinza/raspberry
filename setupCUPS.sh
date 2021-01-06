sudo apt-get install cups
echo The first thing to do is add the pi user to the lpadmin group. This group will allow the pi user to access the administrative functions of CUPS without needing to use the superuser.
sudo usermod -a -G lpadmin pi
echo ensure that it runs well on the home network and that is to make CUPS accessible across your whole network, at the moment it will block any non-localhost traffic
sudo cupsctl --remote-any
sudo systemctl restart cups
hostname -I
echo port 631


