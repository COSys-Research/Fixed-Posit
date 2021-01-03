
################# PARAMS ############
output_path     = "/home/manuawasthi/OpenBLAS/benchmark/outputs"

apps = ["saxpby", "saxpy", "sdot", "sgemm", "sgemv", "sger", "sscal", "sspmv", "sspr2", "sspr", "ssymm", "ssymv", "ssyr2", "ssyr2k", "ssyr", "ssyrk", "stpmv", "stpsv", "strmm", "strmv", "strsm", "strsv"]


runFixedPosit = True
low_bitwidth = 18
high_bitwidth = 32
bitwidth_step  = 2

low_regime_bits = 2
high_regime_bits = 2
regime_step = 1

low_exponent_bits = 6
high_exponent_bits = 6
exponent_step = 1
################# PARAMS ############

############################################################
def get_avg_rel_error(golden_output_filename, approx_output_filename):
    golden_file = open(golden_output_filename, "r")
    approx_file = open(approx_output_filename, "r")

    total_err  = 0
    line_count = 0
    while True:
        gold_line = golden_file.readline()
        approx_line = approx_file.readline()
        if not gold_line:
            break
        golden_val = float(gold_line.strip())
        approx_val = float(approx_line.strip())
        if(golden_val != 0):
            err      = 100*abs(golden_val - approx_val)/abs(golden_val)
        else:
            err      = abs(golden_val - approx_val)
        total_err += err
        line_count += 1
    avg_rel_err = total_err/line_count
    golden_file.close()
    approx_file.close()
    return avg_rel_err
#############################################################



if __name__ == "__main__":
    err_file = open("comphrehensive_error_openblas.csv","w")
    err_file.write(f"Workload")
    if runFixedPosit:
        for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
            for r in range(low_regime_bits, high_regime_bits+1, regime_step):
                for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                    err_file.write(f", {n}_{r}_{es}")
    err_file.write("\n")

    for app in apps:
        err_file.write(f"{app} ")
        if(runFixedPosit):
            for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
                for r in range(low_regime_bits, high_regime_bits+1, regime_step):
                    for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                        err_file.write(f", {get_avg_rel_error(f'{output_path}/{app}_ieee_res.txt', f'{output_path}/{app}_{n}_{r}_{es}_res.txt')}")
        err_file.write("\n")
    err_file.close()




                                

                        

    