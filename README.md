# PaPiRus
Resources for PaPiRus ePaper eInk display

# Setup PaPiRus
```bash
# Run this line and PaPiRus will be setup and installed
curl https://goo.gl/i1Imel | sudo bash
```

# Manually Setup PaPiRus

```bash
sudo apt-get install python-imaging
git clone https://github.com/PiSupply/PaPiRus.git
cd PaPiRus
sudo python setup.py install    # Install PaPirRus python library
papirus-setup    # Install drivers and setup epaper
```
