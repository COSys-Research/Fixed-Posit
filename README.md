# Fixed-Posit

## Description

This repository contains code used in experiments of the paper "Fixed-Posit: A Floating-Point Representation for Error-Resilient Applications" published in IEEE Transactions on Circuits and Systems II.

The directory structure is as follows:
- pintool: Contains the pintool that replaces single-precision IEEE-754 multiplications with fixed-posit multiplications
- scripts: Contains various scripts used to tun experiments 

## How to setup?
- Download [Intel Pin](https://software.intel.com/content/www/us/en/develop/articles/pin-a-dynamic-binary-instrumentation-tool.html). Our pintool is tested with Pin 3.17.
```bash
# Download this repo
git clone https://github.com/COSys-Research/Fixed-Posit.git

# Copy the pintools folder inside Pin's tools folder
# $PIN_HOME is set to the root directot of Intel Pin
cp -r Fixed-Posit/pintool/ $(PIN_HOME)/source/tools/

#Build the pintools
cd $(PIN_HOME)/source/tools/pintool
make
# This would create a obj-intel64 or obj-ia32 folder with *.so files depending on your machine's architecture.
```

## Contributors
- [Sumit Walia](https://github.com/sumit-walia)
- [Varun Gohil](https://github.com/varungohil)
