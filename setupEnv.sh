cd ~
python3 -m venv wx
source ~/wx/bin/activate
sudo apt-get install mupdf mupdf-tools libcups2-dev
pip3 install pycups
mv ~/Downloads/wxPython-4.0.7.post2.tar.gz .
tar xf wxPython-4.0.7.post2.tar.gz
sudo apt-get install python3.7-dev
cd wxPython-4.0.7.post2
pip3 install -r requirements.txt
python3 build.py build bdist_wheel --jobs=1 
cd ~/wxPython-4.0.7.post2/dist
pip3 install wxPython-4.0.7.post2-cp37-cp37m-linux_armv7l.whl
pip3 install wiringpi nfcpy
sudo apt-get install lirc
sudo mv /etc/lirc/lirc_options.conf.dist /etc/lirc/lirc_options.conf
sudo apt-get install lirc
echo edit /etc/lirc/lirc_options.conf to add driver =default and device=/dev/lirc0
sudo mv /etc/lirc/lircd.conf.dist /etc/lirc/lircd.conf
