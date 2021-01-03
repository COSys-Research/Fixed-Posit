
 
#################  PATHS ############
openblas_benchmark_path   = "/home/manuawasthi/OpenBLAS/benchmark"
pin_root        = "/home/manuawasthi/pin_kit"
pintool_path    = "/home/manuawasthi/pin_kit/source/tools/pintools/obj-intel64"
output_path     = "/home/manuawasthi/OpenBLAS/benchmark/outputs"
################# PATHS ############

################# Pintool Params ############
toLog = 1   # 1 for True, 0 for False
log_folder      = "/home/manuawasthi/OpenBLAS/benchmark/logs"
################# Pintool Params ############

################# Fixed-Posit Params ############
runFixedPositMul = True

low_bitwidth = 18
high_bitwidth = 32
bitwidth_step  = 2

low_regime_bits = 2
high_regime_bits = 2
regime_step = 1

low_exponent_bits = 6
high_exponent_bits = 6
exponent_step = 1
################# Fixed-Posit Params ############

################# OPENBLAS ############
apps = ["saxpby", "saxpy", "sdot", "sgemm", "sgemv", "sger", "sscal", "sspmv", "sspr2", "sspr", "ssymm", "ssymv", "ssyr2", "ssyr2k", "ssyr", "ssyrk", "stpmv", "stpsv", "strmm", "strmv", "strsm", "strsv"]

low_input_size = 200
high_input_size = 201
step_input_size = 2

useRandomInputs = 0
################# OPENBLAS ############


script = open(f"{openblas_benchmark_path}/run_openblas_exps.sh", "w")

script.write("echo 'Experiments initiated'\n")
for app in apps:
    script.write(f"{openblas_benchmark_path}/{app}.goto 1 {low_input_size} {high_input_size} {step_input_size}\n")
    script.write(f"mv {openblas_benchmark_path}/{app}_res.txt {output_path}/{app}_ieee_res.txt\n")
script.write("echo 'IEEE outputs generated'\n")

if(runFixedPositMul):    
    for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
        for r in range(low_regime_bits, high_regime_bits+1, regime_step):
            for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                for app in apps:
                    script.write(f"{pin_root}/pin -t {pintool_path}/fixedpositmul.so -n {n} -r {r} -e {es} -l {toLog} -o {log_folder}/log_{app}_{n}_{r}_{es}.txt -- {openblas_benchmark_path}/{app}.goto {useRandomInputs} {low_input_size} {high_input_size} {step_input_size}\n")
                    script.write(f"mv {openblas_benchmark_path}/{app}_res.txt {output_path}/{app}_{n}_{r}_{es}_res.txt\n")                   
                    script.write(f"echo '{n}_{r}_{es} on {app} done'\n")

script.close()


