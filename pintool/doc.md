# fixedpositmul Pintool Documentation

## How to build?
- Download [Intel Pin](https://software.intel.com/content/www/us/en/develop/articles/pin-a-dynamic-binary-instrumentation-tool.html). Our pintool is tested with Pin 3.17.
```bash
# Download this repo
git clone https://github.com/COSys-Research/Fixed-Posit.git

# Copy the pintools folder inside Pin's tools folder
# $PIN_HOME is set to the root directot of Intel Pin
cp -r Fixed-Posit/pintool/ $(PIN_HOME)/source/tools/

#Build the fixedpositmul pintool
cd $(PIN_HOME)/source/tools/pintool
make
# This would create a obj-intel64 or obj-ia32 folder with fixedpositmul.so file depending on your machine's architecture.
```

## How to use?
After building you can use the pintools in the same way any other pintool is used. For a 64 bit machine, the coomand would be as follows:
```bash
$(PIN_HOME)/pin -t $(PIN_HOME)/source/tools/pintools/obj-intel64/fixedpositmul.so -n 32 -e 6 -r 2 -l 1 -o operandlog.out -- <path_to_app>
```

### Arguments to fixedpositmul pintool
The pintool has 5 arguments:
- n : To specify the bit-width of the fixed-posit (default: 32)
- e : To specify exponent size of fixed-posit (default: 6)
- r : To specify regime size of fixed-posit (default: 2)
- l : To specify wheter to log the multiplication operands or not (default: 0). For this argument, 1 means log, 0 means don't log.
- o : To specify the name of log file if we want to log the multiplication operands (default: operandlog.out)

### Format of generated log files
<operand\_1> <operand\_2> <product of operand\_1 and operand\_2>

All numbers of the trace are in single precision IEEE-754 format (type float)  

## Analysis Routine
The analysis routine of this pintool is ```posit_multiply```. The routine takes in the operands of multiplications having type float.
It then converts the operands into fixed-posit format of the specified configuration and perform fixed-posit multiplication. 
Finally it converts the result of multiplication back into type float and returns it.
