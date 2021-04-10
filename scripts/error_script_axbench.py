import os
import cv2 
import numpy as np 
from math import log10, sqrt 
from skimage.metrics import structural_similarity as ssim

################# PATHS ############
axbench_root    = " "

apps = ["blackscholes", "fft", "inversek2j", "jmeint", "jpeg", "kmeans", "sobel"]

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
################# PATHS ############

############################################################
def get_error(cmd):
    try:
        stdout_output = os.popen(cmd).read()
        lst = stdout_output.split(":")
        error_line = lst[1].strip()
        return float(error_line[:-4])
    except Exception as e:
        print(e)
        print(cmd)
        # print(stdout_output)
        # print(lst)
        exit(0)

def PSNR(original, compressed): 
    mse = np.mean((original - compressed) ** 2) 
    if(mse == 0):  # MSE is zero means no noise is present in the signal . 
                  # Therefore PSNR have no importance. 
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse)) 
    return psnr 
 
def RMSE(original, compressed):
	return np.sqrt(np.mean((original - compressed) ** 2))


#############################################################


if __name__ == "__main__":
    err_file = open("comphrehensive_error_axbench.csv","w")
    err_file.write(f"Workload, Input, Error Metric")
    if runFixedPosit:
        for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
            for r in range(low_regime_bits, high_regime_bits+1, regime_step):
                for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                    err_file.write(f", {n}_{r}_{es}")
    err_file.write("\n")

    for app in apps:
        if app in ["blackscholes", "fft", "inversek2j"]:
            scripts_path = f"{axbench_root}/applications/{app}/scripts"
            for folder in ["test"]:
                for qos_file in ["qos.py", f"qos_{app}.py"]:
                    err_file.write(f"{app}, {folder}, {qos_file} ")
                    if(runFixedPosit):
                        for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
                            for r in range(low_regime_bits, high_regime_bits+1, regime_step):
                                for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                                    cmd = f"python {scripts_path}/{qos_file} {axbench_root}/applications/{app}/{folder}.data/output/{app}_ieee_output.txt {axbench_root}/applications/{app}/{folder}.data/output/{app}_{n}_{r}_{es}_i{folder}_output.txt"
                                    err_file.write(f", {100*get_error(cmd)}")
                    err_file.write("\n")
        elif app in ["jmeint"]:
            scripts_path = f"{axbench_root}/applications/{app}/scripts"
            for folder in ["test"]:
                err_file.write(f"{app}, {folder}, qos.py ")
                if(runFixedPosit):
                    for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
                        for r in range(low_regime_bits, high_regime_bits+1, regime_step):
                            for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                                cmd = f"python {scripts_path}/qos.py {axbench_root}/applications/{app}/{folder}.data/output/{app}_ieee_output.txt {axbench_root}/applications/{app}/{folder}.data/output/{app}_{n}_{r}_{es}_i{folder}_output.txt"
                                err_file.write(f", {100*get_error(cmd)}")
                err_file.write("\n")
        elif app in ["jpeg"]:
            for err_metric in ["RMSE", "PSNR", "SSIM"]:
                for imgnum in range(1,38):
                    if imgnum != 29:
                        err_file.write(f"{app}, {imgnum}, {err_metric}")
                        if imgnum <= 3:
                            folder = "train"
                        else:
                            folder = "test"
                        ieee_img_path = f"{axbench_root}/applications/{app}/{folder}.data/output/jpeg_ieee_i{imgnum}_output.jpg" 
                        ieee_img      = cv2.imread(ieee_img_path)
                        if(runFixedPosit):
                            for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
                                for r in range(low_regime_bits, high_regime_bits+1, regime_step):
                                    for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                                        approx_img_path = f"{axbench_root}/applications/{app}/{folder}.data/output/jpeg_{n}_{r}_{es}_i{imgnum}_output.jpg" 
                                        approx_img      = cv2.imread(approx_img_path)
                                        if err_metric == "RMSE":
                                            err_file.write(f", {RMSE(ieee_img, approx_img)}")
                                        elif err_metric == "PSNR":
                                            err_file.write(f", {PSNR(ieee_img, approx_img)}")
                                        elif err_metric == "SSIM":
                                            err_file.write(f", {ssim(ieee_img, approx_img, multichannel=True)}")

                                        # err_file.write(f", {PSNR(ieee_img, approx_img)}")
                        err_file.write("\n")
        elif app in ["kmeans", "sobel"]:
            for err_metric in ["rmse","psnr"]: 
                for imgnum in range(1,38):
                    if imgnum != 29:
                        err_file.write(f"{app}, {imgnum}, RMSE ")
                        if imgnum <= 3:
                            folder = "train"
                        else:
                            folder = "test"
                        if(runFixedPosit):
                            for n in range(low_bitwidth, high_bitwidth+1, bitwidth_step):
                                for r in range(low_regime_bits, high_regime_bits+1, regime_step):
                                    for es in range(low_exponent_bits, high_exponent_bits+1, exponent_step):
                                        cmd = f"{axbench_root}/applications/{app}/src/{app}_{err_metric}.out {axbench_root}/applications/{app}/{folder}.data/output/{app}_ieee_i{imgnum}_output.rgb {axbench_root}/applications/{app}/{folder}.data/output/{app}_{n}_{r}_{es}_i{imgnum}_output.rgb"
                                        err_file.write(f", {get_error(cmd)}")
                        err_file.write("\n")

    err_file.close()




                                

                        

    
