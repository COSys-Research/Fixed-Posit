# Documentation for multiplier_verilog_generator.py
This script generates verilog codes for the specified fixed-posit multipliers.

## Parameters
- `codes_path`: Set the variable as the absolute path to the directory in which you want the generated Verilog codes to be stored.
- `min_bitlength`: The lowest bitwidth fixed-posit configuration you want to generate verilog code for.
- `max_bitlength`: The highest bitwidth fixed-posit configuration you want to generate verilog code for.
- `step_bitlength`: The difference of two successive bitwidths in the list of fixed-posit configurations you want  to generate verilog code for. 
- `min_es`: The lowest exponent size among fixed-posit configurations you want to generate verilog code for.
- `max_es`: The highest exponent size among fixed-posit configurations you want to generate verilog code for.
- `step_es`: The difference of two successive exponent sizes in the list of fixed-posit configurations you want  to generate verilog code for.
- `min_regime`: The lowest regime size among fixed-posit configurations you want to generate verilog code for.
- `max_regime`: The highest regime size among fixed-posit configurations you want to generate verilog code for.
- `step_regime`: The difference of two successive regime sizes in the list of fixed-posit configurations you want  to generate verilog code for.

## Naming Convention of generated Verilog files
 fxp\_<bitwidth>\_<exponent\_size>\_<regime\_size>.v
