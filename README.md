# PaPiRus
Resources for PaPiRus ePaper eInk display

# Setup PaPiRus
```bash
# Run this line and PaPiRus will be setup and installed
curl https://goo.gl/i1Imel | sudo bash
```

# Manually Setup PaPiRus

#### Install Python API
```bash

# Install dependencies
sudo apt-get install python-imaging

git clone https://github.com/PiSupply/PaPiRus.git
cd PaPiRus
sudo python setup.py install    # Install PaPirRus python library
```

#### Install Driver (Option 1)
```bash
papirus-setup    # This will auto install the driver
````

#### Install Driver (Option 2)
```bash
# Install fuse driver
sudo apt-get install libfuse-dev -y

sudo mkdir /tmp/papirus
cd /tmp/papirus
git clone https://github.com/repaper/gratis.git

cd /tmp/papirus/gratis-master/PlatformWithOS
make rpi-epd_fuse
sudo make rpi-install
sudo service epd-fuse start
```
