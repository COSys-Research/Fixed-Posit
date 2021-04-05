#################  PATHS ############
axbench_root    = "/home/manuawasthi/axbench"
pin_root        = "/home/manuawasthi/pin_kit"
pintool_path    =  "/home/manuawasthi/pin_kit/source/tools/pintools/obj-intel64"
################# PATHS ############

################# Pintool Params ############
toLog = 1   # 1 for True, 0 for False
log_folder      = "/home/manuawasthi/axbench/logs"
################# Pintool Params ############


################# Fixed-Posit Params ############
runFixedPosit = True

low_bitwidth = 18;
high_bitwidth = 32;
bitwidth_step  = 2

low_regime_bits = 2
high_regime_bits = 2
regime_step = 1

low_exponent_bits = 6
high_exponent_bits = 6
exponent_step = 1
################# Fixed-Posit Params ############

################# APPS ############
apps = ["blackscholes", "fft", "inversek2j", "jmeint", "jpeg", "kmeans", "sobel"]

input_dict = {
    "blackscholes_train" : "blackscholesTrain_100K.data", 
    "blackscholes_test"  : "blackscholesTest_200K.data", 
    "inversek2j_train"   : "theta_100K.data",
    "inversek2j_test"    : "theta_1000K.data",
    "jmeint_train"       : "jmeint_10K.data",
    "jmeint_test"        : "jmeint_1000K.data",  
    "fft_train"          : "2048",
    "fft_test"           : "2048",  
}

################# APPS ############


script = open("run_axbench_exps.sh", "w")

script.write("echo 'Experiments initiated'\n")
for app in apps:
    if app in ["blackscholes", "jmeint", "inversek2j"]:
        # script.write(f"{axbench_root}/applications/{app}/src/{app}.out {axbench_root}/applications/{app}/train.data/input/{input_dict[app + '_train']} {axbench_root}/applications/{app}/train.data/output/{app}_ieee_itrain_output.txt\n")
        script.write(f"{axbench_root}/applications/{app}/src/{app}.out {axbench_root}/applications/{app}/test.data/input/{input_dict[app + '_test']} {axbench_root}/applications/{app}/test.data/output/{app}_ieee_itest_output.txt\n")
    elif app in ["fft"]:
        # script.write(f"{axbench_root}/applications/{app}/src/{app}.out {input_dict[app + '_train']} {axbench_root}/applications/{app}/train.data/output/{app}_ieee_itrain_output.txt\n")
        script.write(f"{axbench_root}/applications/{app}/src/{app}.out {input_dict[app + '_test']} {axbench_root}/applications/{app}/test.data/output/{app}_ieee_itest_output.txt\n")
    elif app in ["kmeans", "jpeg", "sobel"]:
        if app == "kmeans" or app == "sobel":
            output_format = "rgb"
        else:
            output_format = "jpg"
        for imgnum in range(1,38):
            if(imgnum <= 3):
                folder = "train"
            else:
                folder = "test"
            script.write(f"{axbench_root}/applications/{app}/src/{app}.out {axbench_root}/applications/{app}/{folder}.data/input/{imgnum}.rgb {axbench_root}/applications/{app}/{folder}.data/output/{app}_ieee_i{imgnum}_output.{output_format}\n")

script.write("echo 'IEEE outputs generated'\n")


if(runFixedPosit):    
    for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
        for r in range(low_regime_bits, high_regime_bits+1, regime_step):
            for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                for app in apps:
                    if app in ["blackscholes", "jmeint", "inversek2j"]:
                        # script.write(f"{pin_root}/pin -t {pintool_path}/fixedpositmul.so -n {n} -e {es} -r {r} -l {toLog} -o {log_folder}/log_{app}_{n}_{r}_{es}_itrain.txt -- {axbench_root}/applications/{app}/src/{app}.out {axbench_root}/applications/{app}/train.data/input/{input_dict[app + '_train']} {axbench_root}/applications/{app}/train.data/output/{app}_{n}_{r}_{es}_itrain_output.txt\n")
                        script.write(f"{pin_root}/pin -t {pintool_path}/fixedpositmul.so -n {n} -e {es} -r {r} -l {toLog} -o {log_folder}/log_{app}_{n}_{r}_{es}_itest.txt -- {axbench_root}/applications/{app}/src/{app}.out {axbench_root}/applications/{app}/test.data/input/{input_dict[app + '_test']} {axbench_root}/applications/{app}/test.data/output/{app}_{n}_{r}_{es}_itest_output.txt\n")
                    elif app in ["fft"]:
                        # script.write(f"{pin_root}/pin -t {pintool_path}/fixedpositmul.so -n {n} -e {es} -r {r} -l {toLog} -o {log_folder}/log_{app}_{n}_{r}_{es}_itrain.txt -- {axbench_root}/applications/{app}/src/{app}.out {input_dict[app + '_train']} {axbench_root}/applications/{app}/train.data/output/{app}_{n}_{r}_{es}_itrain_output.txt\n")
                        script.write(f"{pin_root}/pin -t {pintool_path}/fixedpositmul.so -n {n} -e {es} -r {r} -l {toLog} -o {log_folder}/log_{app}_{n}_{r}_{es}_itest.txt -- {axbench_root}/applications/{app}/src/{app}.out {input_dict[app + '_test']} {axbench_root}/applications/{app}/test.data/output/{app}_{n}_{r}_{es}_itest_output.txt\n")
                    elif app in ["kmeans", "jpeg", "sobel"]:
                        if app == "kmeans" or app == "sobel":
                            output_format = "rgb"
                        else:
                            output_format = "jpg"
                        for imgnum in range(1,38):
                            if(imgnum <= 3):
                                folder = "train"
                            else:
                                folder = "test"
                            script.write(f"{pin_root}/pin -t {pintool_path}/fixedpositmul.so -n {n} -e {es} -r {r} -l {toLog} -o {log_folder}/log_{app}_{n}_{r}_{es}_i{imgnum}.txt -- {axbench_root}/applications/{app}/src/{app}.out {axbench_root}/applications/{app}/{folder}.data/input/{imgnum}.rgb {axbench_root}/applications/{app}/{folder}.data/output/{app}_{n}_{r}_{es}_i{imgnum}_output.{output_format}\n")
                    else:
                        print(f"No conditions for executing {app} specified")
                    script.write(f"echo '{n}_{r}_{es} on {app} done'\n")
script.close()
