from bitstring import Bits


codes_path = "/home/manuawasthi/codes"

########### Fixed-Posit Params###########
min_bitlength = 18
max_bitlength = 32
step_bitlength = 2

min_es = 6
max_es = 6
step_es = 1

min_regime = 2
max_regime = 2
step_regime = 1
########### Fixed-Posit Params###########


for n in range(min_bitlength, max_bitlength+1, step_bitlength):
    for es in range(min_es, max_es+1, step_es):
        for r in range(min_regime, max_regime+1, step_regime):
            code = open(f"{codes_path}/fxp_{n}_{es}_{r}.v", "w")
            decoder_code = """always@(*) begin\ncase(number)\n"""
            encoder_code = """always@(*) begin\ncase(pregime)\n"""
            for regime_sequence_bit in ["0", "1"]:
                if regime_sequence_bit == "0":
                    complement_bit = "1"
                else:
                    complement_bit = "0"
                for i in range(1,r+1):
                    regime_string = regime_sequence_bit*i + complement_bit*(r-i)
                    if regime_sequence_bit == "0":
                        k = -1*i 
                    else:
                        k = i - 1
                    k_string = str(Bits(int = k, length = r).bin)
                    if regime_sequence_bit == "0":
                        if i != r:
                            decoder_code = decoder_code + f"    {r}'b{regime_string} : p_regime = {r}'b{k_string};\n"
                        else:
                            decoder_code = decoder_code + f"    default : p_regime = {r}'b{k_string};\n"
                    if i == r and regime_sequence_bit == "1":
                        encoder_code = encoder_code + f"    default : result_out = {r}'b{regime_string};\n"
                    else:
                        encoder_code = encoder_code + f"    {r}'b{k_string} : result_out = {r}'b{regime_string};\n"
            decoder_code = decoder_code + "endcase\nend\n"
            encoder_code = encoder_code + "endcase\nend\n"
            code.write("`timescale 1ns / 1ps\n")

            code.write("`define N " + str(n) + "\n")
            code.write("`define es " + str(es) +"\n")
            code.write("`define regime " + str(r) + "\n")
            code.write("module posit(a,psign,pregime,pexp,pfrac,pzero,pinf);"+"\n")
            code.write("    input [`N-1:0]a;"+"\n")
            code.write("    output psign;"+"\n")
            code.write("    output [`regime-1:0]pregime;"+"\n")
            code.write("    output [`es-1:0]pexp;"+"\n")
            code.write("    output [`N-`es-`regime-2:0]pfrac;"+"\n")
            code.write("    output pzero;"+"\n")
            code.write("    output pinf;"+"\n")
            code.write("    wire [`N-2:0]x;"+"\n")
            code.write("    wire [`regime-1:0]number;"+"\n")
            code.write("    reg [`regime-1:0]p_regime;\n"+"\n")
            code.write("//-----------------------sign----------------------"+"\n")
            code.write("    assign psign = a[`N-1];"+"\n")
            code.write("    assign x = psign? ~a[`N-2:0] + 1'b1: a[`N-2:0];\n"+"\n")
            code.write("//-----------------------inf\zero check----------------------"+"\n")
            code.write("    assign pzero = psign ? 1'b0:( x[`N-2:0]==`N-1'b0 ? 1'b1:1'b0);"+"\n")
            code.write("    assign pinf = psign ? ( x[`N-2:0]==`N-1'b0 ? 1'b1:1'b0):1'b0;\n"+"\n")
            code.write("//-----------------------regime----------------------"+"\n")
            code.write("    assign number = x[`N-2]?~x[`N-2:`N-2-`regime-1]:x[`N-2:`N-2-`regime-1];\n"+"\n")
           
            code.write("\n" + decoder_code + "\n")

            code.write("    assign pregime = x[`N-1]?p_regime-1'b1:~p_regime+1'b1;"+"\n")
            code.write("//-----------------------expo----------------------"+"\n")
            code.write("    assign pexp = x[`N-`regime-2:`N-`regime-`es-1];"+"\n")
            code.write("//-----------------------frac-----------------------"+"\n")
            code.write("    assign pfrac = x[`N-`regime-`es-2:0];\n"+"\n")
            code.write("endmodule\n")
            code.write("//---------posit multiplication------------------------"+"\n")
            code.write("module pmult(a,b,out,clk,reset,pinf,pzero);"+"\n")
            code.write("    input [`N-1:0]a,b;"+"\n")
            code.write("    input clk,reset;"+"\n")
            code.write("    output reg [`N-1:0]out;"+"\n")
            code.write("    output pinf,pzero;"+"\n")
            code.write("    reg [`N-1:0]x,y;"+"\n")
            code.write("    wire [`N-1:0]OUT;"+"\n")
            code.write("    wire [`N-1:0]result;"+"\n")
            code.write("    wire [2*(`N-`es-`regime)-1:0]mult_out;"+"\n")
            code.write("    reg [`regime-1:0]result_out;"+"\n")
            code.write("    wire psign;"+"\n")
            code.write("    wire [`regime-1:0]pregime;"+"\n")
            code.write("    wire [`regime+`es-1:0]a_exp,b_exp,t_exp;"+"\n")
            code.write("    wire [`N-`es-`regime-2:0]pfrac;"+"\n")
            code.write("    wire a_psign,b_psign;"+"\n")
            code.write("    wire [`regime-1:0]a_pregime,b_pregime;"+"\n")
            code.write("    wire [`es-1:0]a_pexp,b_pexp;"+"\n")
            code.write("    wire [`N-`es-`regime-2:0]a_pfrac,b_pfrac;"+"\n")
            code.write("    wire a_pzero,a_pinf,b_pzero,b_pinf;\n"+"\n")
            code.write("always@(posedge clk) begin"+"\n")
            code.write("if(reset) begin"+"\n")
            code.write("    x <= `N'b0;"+"\n")
            code.write("    y <= `N'b0;"+"\n")
            code.write("    out <= `N'b0;	end"+"\n")
            code.write("else begin"+"\n")
            code.write("    x <= a;"+"\n")
            code.write("    y <= b;"+"\n")
            code.write("    out <= OUT;	end"+"\n")
            code.write("end"+"\n")
            code.write("    posit a1(x,a_psign,a_pregime,a_pexp,a_pfrac,a_pzero,a_pinf);"+"\n")
            code.write("    posit b1(y,b_psign,b_pregime,b_pexp,b_pfrac,b_pzero,b_pinf);"+"\n")

            code.write("    assign pinf = (a_pinf | b_pinf) ? 1'b1 : 1'b0;"+"\n")
            code.write("    assign pzero = ~(a_pinf|b_pinf)&(a_pzero|b_pzero) ? 1'b1 : 1'b0;\n"+"\n")

            code.write("//-----------------------sign----------------------"+"\n")
            code.write("    assign psign = a_psign ^ b_psign;\n"+"\n")
            code.write("//-----------------------frac----------------------"+"\n")
            code.write("    assign result[`N-`es-`regime-2:0] = mult_out[2*(`N-`es-`regime)-1]? mult_out[2*(`N-`es-`regime)-1-1:2*(`N-`es-`regime)-1-(`N-`es-`regime-1)] : mult_out[2*(`N-`es-`regime)-1-1-1:2*(`N-`es-`regime)-1-(`N-`es-`regime-1)-1];\n"+"\n")
            code.write("//-----------------------total_exp----------------------"+"\n")
            code.write("    assign a_exp = {a_pregime,`es'b0} + a_pexp;"+"\n")
            code.write("    assign b_exp = {b_pregime,`es'b0} + b_pexp;"+"\n")
            code.write("    assign t_exp = a_exp + b_exp + mult_out[2*(`N-`es-`regime)-1];"+"\n")
            code.write("    assign pregime = t_exp[`es+`regime-1:`es];\n"+"\n")

            code.write("    assign result[`N-`regime-2:`N-`es-`regime-1] = t_exp[`es-1:0];"+"\n")

            code.write("\n" + encoder_code + "\n")

            code.write("    assign result[`N-1] = psign;"+"\n")
            code.write("    assign result[`N-2:`N-`regime-1] = result_out;"+"\n")
            code.write("    assign OUT = result[`N-1]? {result[`N-1],~result[`N-2:0]+1'b1} : result;"+"\n")
            code.write("endmodule"+"\n")