# Fixed-Posit

## Description

This repository contains code used in experiments of the paper "Fixed-Posit: A Floating-Point Representation for Error-Resilient Applications" published in IEEE Transactions on Circuits and Systems II.

The directory structure is as follows:
- pintool: Contains the pintool that replaces single-precision IEEE-754 multiplications with fixed-posit multiplications
- scripts: Contains various scripts used to run experiments 

## How to setup?
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
For the experiments we will use a modified version of OpenBLAS repo. The modifications allow OpenBLAS benchmarks to read inputs from the files rather than generating inputs randomly.
```bash
#Download this modified OpenBLAS repo 
git clone https://github.com/varungohil/OpenBLAS.git

# Compile OpenBLAS and its benchmarks for NEHALEM target
cd $(OPENBLAS_PATH)

make TARGET=NEHALEM

cd $(OPENBLAS_PATH)/benchmark/

make TARGET=NEHALEM
```


Create two new directories somewhere on your system: one to store the outputs of OpenBLAS benchmarks and the other to store the logs of multiplication operands generated by the pintool.
```bash
cd $(OPENBLAS_PATH)/benchmark/

# outputs directory to store the outputs/results of the OpenBLAS benchmarks
mkdir openblas_outputs

# logs directory to store the logs of mutliplication operands generated by the fixedpositmul pintool
mkdir openblas_logs
```

To setup AxBench, execute the commands given below
```
#Clone AxBench
git clone https://bitbucket.org/act-lab/axbench.git

cp Fixed-Posit/scripts/compile_axbench.sh $(AXBENCH_PATH)/applications/
cp Fixed-Posit/scripts/qos_blackscholes.py $(AXBENCH_PATH)/applications/blackscholes/scripts/
cp Fixed-Posit/scripts/qos_fft.py $(AXBENCH_PATH)/applications/fft/scripts/
cp Fixed-Posit/scripts/qos_inversek2j.py $(AXBENCH_PATH)/applications/inversek2j/scripts/

cd $(AXBENCH_PATH)/applications/
sh compile_axbench.sh

cd ..

# logs directory to store the logs of mutliplication operands generated by the fixedpositmul pintool
mkdir axbench_logs
```

Install [bitstring python package](https://pypi.org/project/bitstring/). Required for generating Verilog codes for fixed-posit multiplier.
```
pip3 install bitstring
pip3 install opencv-python
# Update pip
python -m pip install -U pip
# Install scikit-image
python -m pip install -U scikit-image
```

## How to run?
### How to get error?
First, edit the `openblas_benchmark_path`, `pin_root`, `pintool_path`, `log_folder` variables in the scripts `script_maker_openblas.py` and `error_script_openblas.py` to point to the appropriate directories in your system.

Next run the following:
```bash
python3 script_maker_openblas.py
# Running this would generate a shell script run_openblas_exps.sh in the benchmark directory of OpenBLAS 
cd (OPENBLAS_PATH)/benchmark/

export OPENBLAS_NUM_THREADS=1
# Since pintool only supports single-threaded applications 

sh run_openblas_exps.sh
# Running this shell scripts will run the fixedpositmul pintool with OpenBLAS benchmark and store the results and logs in outputs and logs folder respectively. 

python3 error_script_openblas.py
# Running this scripts will compute the average relative error for all workloads for all fixed-posit configurations.
```

The computed errors are reported in the generated `comphrehensive_error_openblas.csv` file.

### How to get power?
TODO

### How to get area and delay?
TODO

## Detailed Documentation
- [fixedpositmul pintool](https://github.com/COSys-Research/Fixed-Posit/blob/master/pintool/README.md)
- [Individual scripts](https://github.com/COSys-Research/Fixed-Posit/tree/master/scripts/docs)

## Contributors
- [Sumit Walia](https://github.com/sumit-walia)
- [Varun Gohil](https://github.com/varungohil)
