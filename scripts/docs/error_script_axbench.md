# Documentation for error_script_axbench.py

The script computes the errors in the results of benchmarks when running them with the fixedpositmul pintool.
It generates a file named _comphrehensive\_error\_axbench.csv_ to report the errors.

## Parameters
- `axbench_root` : Set the variable as the absolute path to the directory AxBench benchmark as per your system.
- `apps` : A list of benchmarks for which to compute the error. You can edit this list if you want to compute errors for more/less benchmarks.
- `low_bitwidth` : The lowest bitwidth fixed-posit configuration you want to compute error for
- `high_bitwidth` : The highest bitwidth fixed-posit configuration you want to compute error for
- `bitwidth_step` : The difference of two successive bitwidths in the list of your fixed-posit configurations
- `low_regime_bits`: The lowest regime size among the fixed-posit configurations you want to compute error for
- `high_regime_bits`: The highest regime size among the fixed-posit configurations you want to compute error for
- `regime_step`: The difference of two successive regime sizes in the list of your fixed-posit configurations
- `low_exponent_bits`: The lowest exponent size among the fixed-posit configurations you want to compute error for
- `high_exponent_bits`: The highest exponent size among the fixed-posit configurations you want to compute error for
- `exponent_step`: The difference of two successive exponent sizes in the list of your fixed-posit configurations

We recommend not changing any other parameters in the script.
