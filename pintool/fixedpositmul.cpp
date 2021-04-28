


// Intel ISA Manual Ref. Link
// https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.pdf
//Latest Ref: https://software.intel.com/en-us/download/intel-64-and-ia-32-architectures-sdm-combined-volumes-1-2a-2b-2c-2d-3a-3b-3c-3d-and-4


#include <iostream>
#include <fstream>
#include <cmath>
#include "pin.H"


using std::cerr;
using std::ofstream;
using std::ios;
using std::string;
using std::endl;


#define XO(opcode) (XED_ICLASS_##opcode)



/* ===================================================================== */
/* Commandline Switches */
/* ===================================================================== */

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool", "o", "operandlog.out", "specify output file name");
KNOB<UINT32> KnobBitWidth(KNOB_MODE_WRITEONCE, "pintool", "n", "32", "Bitwidth of fixed-posit");
KNOB<UINT32> KnobExponentSize(KNOB_MODE_WRITEONCE, "pintool", "e", "6", "Exponent Size of fixed-posit");
KNOB<UINT32> KnobRegimeSize(KNOB_MODE_WRITEONCE, "pintool", "r", "2", "Regime Size of fixed-posit");
KNOB<BOOL>   KnobLog(KNOB_MODE_WRITEONCE, "pintool", "l", "0", "To log or not to log, thats the question");

int posit_length;
int es;           
int useed;        //2^es
int regime_len;   
int frc_len;      

FILE *logfile;

float posit_multiply(float op1, float op2)
{
    int op1_sign,  op1_exp, op2_sign, op2_exp, op1_k,  op2_k, op1_e, op2_e;
    // int op1_e_remaining_max, op2_e_remaining_max, op1_frclen, op2_frclen;
    int posit_sign, posit_k, posit_e;
    float posit_f, posit_fnew;
    float op1_f, op2_f, op1_fnew, op2_fnew;
    float result;
    int kmax = regime_len - 1;
    int kmin = -1*regime_len;
    int emax = (int)pow(2.0, es) - 1;

    if(KnobLog)
    {
        fprintf(logfile, "%.14f %.14f", op1, op2);
    }
    
    if(op1 < 0)
    {
        op1_sign = 1;
        op1 = -1*op1;
    }
    else
    {
        op1_sign = 0;
    }
    if(op2 < 0)
    {
        op2_sign = 1;
        op2 = -1*op2;
    }
    else
    {
        op2_sign = 0;
    }
    if(op1 == 0.0)
    {
        result =  0.0;
        if(KnobLog)
        {
            fprintf(logfile, " %.14f\n", result);
        }
        return result;
    }
    if(op2 == 0.0)
    {
        result =  0.0;
        if(KnobLog)
        {
            fprintf(logfile, " %.14f\n", result);
        }
        return result;
    }

    op1_exp = (int)floor(log2(op1));
    op2_exp = (int)floor(log2(op2));
    op1_k   = (int)floor(op1_exp/(float)useed);
    op2_k   = (int)floor(op2_exp/(float)useed);
    if (op1_k > kmax)
    {
        op1_k = kmax;
    }
    else if (op1_k < kmin)
    {
        op1_k = kmin;
    }
    if (op2_k > kmax)
    {
        op2_k = kmax;
    }
    else if (op2_k < kmin)
    {
        op2_k = kmin;
    }

    op1_e = op1_exp - op1_k*useed;
    op2_e = op2_exp - op2_k*useed;

    if(op1_e > emax)
    {
        op1_e = emax;
    }
    if(op2_e > emax)
    {
        op2_e = emax;
    }


    op1_f = (float)op1/pow(2.0, op1_exp);
    op2_f = (float)op2/pow(2.0, op2_exp);
    op1_fnew = op1_f - 1;
    op2_fnew = op2_f - 1;

    for (int i = 1; i < frc_len + 1; i++)
    {
        op1_fnew = op1_fnew -  pow(2.0, (-1*i)) ;
        if (op1_fnew < 0)
        {
            op1_fnew = op1_fnew + pow(2.0, (-1*i));
        }
    }
    for (int i = 1; i < frc_len + 1; i++)
    {
        op2_fnew = op2_fnew - pow(2.0, (-1*i));
        if (op2_fnew < 0)
        {
            op2_fnew = op2_fnew + pow(2.0, (-1*i));
        }
    }

    op1_f = op1_f - op1_fnew;
    op2_f = op2_f - op2_fnew;

   posit_sign = op1_sign + op2_sign;
   if (posit_sign != 1)
   {
       posit_sign = 0;
   }
   
   op1_e = op1_e + op1_k*useed;
   op2_e = op2_e + op2_k*useed;
   
   posit_e = op1_e + op2_e;
   posit_f = op1_f*op2_f;

    

    if (posit_f >= 2)
    {
        posit_f = posit_f/2;
        posit_e = posit_e + 1;
    }

    posit_k = (int)floor(posit_e/(float)useed);

    if (posit_k > kmax)
    {
        posit_k = kmax;
    }
    else if (posit_k < kmin)
    {
        posit_k = kmin;
    }
    
    posit_e = posit_e - posit_k*useed;
    if (posit_e > emax)
    {
        posit_e = emax;
    }

    posit_fnew = posit_f - 1;
    for (int i = 1; i < frc_len + 1; i++)
    {
        posit_fnew = posit_fnew - pow(2.0, (-1*i));
        if (posit_fnew < 0)
        {
            posit_fnew += pow(2.0, (-1*i));
        }
        
    }

    if (posit_sign == 1)
    {
        result = -1*((posit_f - posit_fnew)*pow(2.0, useed*posit_k + posit_e));
    }
    else
    {
        result = (posit_f - posit_fnew)*pow(2.0, useed*posit_k + posit_e);
    }

    if(KnobLog)
    {
        fprintf(logfile, " %.14lf\n", result);
    }

    return result;
}

// This function is called before every instruction is executed
VOID regmemcounter( PIN_REGISTER* src_reg, ADDRINT addr, uint32_t size)
{    
    // fprintf(logfile, "REGMEM ");
    FLT32 val;
    PIN_SafeCopy(&val, (void *)addr, size); 
    src_reg->flt[0] = posit_multiply(src_reg->flt[0], val);
}

VOID regmemcounterp( PIN_REGISTER* src_reg, ADDRINT addr, uint32_t size)
{
    FLT32 val;
    for(unsigned int i=0; i < 4; i++)
    {
        // fprintf(logfile, "MULPS_MEM ");
        PIN_SafeCopy(&val, (void *)(addr + 4*i), 4);
        src_reg->flt[i] = posit_multiply(src_reg->flt[i], val);
    }
}


VOID regregcounter( PIN_REGISTER* src_reg1, PIN_REGISTER* src_reg2)
{
    // fprintf(logfile, "REGREG ");
    src_reg1->flt[0] = posit_multiply(src_reg1->flt[0], src_reg2->flt[0]);
}

VOID regregcounterp( PIN_REGISTER* src_reg1, PIN_REGISTER* src_reg2)
{
    for(unsigned int i=0; i < 4; i++)
    {
        // fprintf(logfile, "MULPS_REG ");
        src_reg1->flt[i] = posit_multiply(src_reg1->flt[i], src_reg2->flt[i]);
    }
}


VOID vmulss_regreg( PIN_REGISTER* src_reg1, PIN_REGISTER* src_reg2, PIN_REGISTER* src_reg3)
{    
    // fprintf(logfile, "VMULSS_REG ");
    src_reg1->flt[0] = posit_multiply(src_reg2->flt[0], src_reg3->flt[0]);
    for(unsigned int i=0; i < 4; i++)
    {
        src_reg1->flt[i] = src_reg2->flt[i];
    }
}

VOID vmulss_regmem( PIN_REGISTER* src_reg1, PIN_REGISTER* src_reg2, ADDRINT addr, uint32_t size)
{    
    // fprintf(logfile, "VMULSS_MEM ");
    FLT32 val;
    PIN_SafeCopy(&val, (void *)addr, size); 
    src_reg1->flt[0] = posit_multiply(src_reg2->flt[0], val);
    for(unsigned int i=0; i < 4; i++)
    {
        src_reg1->flt[i] = src_reg2->flt[i];
    }
}

VOID vmulps_regmem( PIN_REGISTER* src_reg1, PIN_REGISTER* src_reg2, ADDRINT addr, uint32_t size)
{
    FLT32 val;
    for(unsigned int i=0; i < 4; i++)
    {
        // fprintf(logfile, "VMULPS_MEM ");
        PIN_SafeCopy(&val, (void *)(addr + 4*i), 4);
        src_reg1->flt[i] = posit_multiply(src_reg2->flt[i], val);
    }
}

VOID vmulps_regreg( PIN_REGISTER* src_reg1, PIN_REGISTER* src_reg2, PIN_REGISTER* src_reg3)
{
    for(unsigned int i=0; i < 4; i++)
    {
        // fprintf(logfile, "VMULPS_REG ");
        src_reg1->flt[i] = posit_multiply(src_reg2->flt[i], src_reg3->flt[i]);
    }
}


// Pin calls this function every time a new instruction is encountered
VOID Instruction(INS ins, VOID *v)
{
    switch (INS_Opcode(ins))
    {
        case XO(MULSS):
        {
             uint32_t numOperands = INS_OperandCount(ins);
             assert(numOperands == 2);
             assert(INS_OperandWritten(ins, 0));
             REG reg1 = INS_OperandReg(ins, 0);
             if(INS_OperandIsMemory(ins, 1))
             {
                INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)regmemcounter, IARG_REG_REFERENCE, reg1, IARG_MEMORYREAD_EA , IARG_MEMORYREAD_SIZE, IARG_END);
                INS_Delete(ins);
             }
             else
             {
                 REG reg2 = INS_OperandReg(ins, 1);
                 INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)regregcounter, IARG_REG_REFERENCE, reg1, IARG_REG_REFERENCE, reg2, IARG_END);
                 INS_Delete(ins);
             } 
             break;         
        }
        case XO(VMULSS):
        {
             uint32_t numOperands = INS_OperandCount(ins);
             assert(numOperands == 3);
             assert(INS_OperandWritten(ins, 0));
             REG reg1 = INS_OperandReg(ins, 0);
             REG reg2 = INS_OperandReg(ins, 1);
             if(INS_OperandIsMemory(ins, 2))
             {
                 INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)vmulss_regmem, IARG_REG_REFERENCE, reg1, IARG_REG_REFERENCE, reg2, IARG_MEMORYREAD_EA , IARG_MEMORYREAD_SIZE, IARG_END);
                 INS_Delete(ins);
             }
             else
             {
                 REG reg3 = INS_OperandReg(ins, 2);
                 INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)vmulss_regreg, IARG_REG_REFERENCE, reg1, IARG_REG_REFERENCE, reg2, IARG_REG_REFERENCE, reg3, IARG_END);
                 INS_Delete(ins);
             } 
             break;   
        }   
        case XO(MULPS):
        {
             uint32_t numOperands = INS_OperandCount(ins);
             assert(numOperands == 2);
             assert(INS_OperandWritten(ins, 0));
             REG reg1 = INS_OperandReg(ins, 0);
             if(INS_OperandIsMemory(ins, 1))
             {
                 INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)regmemcounterp, IARG_REG_REFERENCE, reg1, IARG_MEMORYREAD_EA , IARG_MEMORYREAD_SIZE, IARG_END);
                 INS_Delete(ins);
             }
             else
             {
                 REG reg2 = INS_OperandReg(ins, 1);
                 INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)regregcounterp, IARG_REG_REFERENCE, reg1, IARG_REG_REFERENCE, reg2, IARG_END);
                 INS_Delete(ins);
             }
             break;              
        }
        case XO(VMULPS):
        {
             uint32_t numOperands = INS_OperandCount(ins);
             assert(numOperands == 3);
             assert(INS_OperandWritten(ins, 0));
             REG reg1 = INS_OperandReg(ins, 0);
             REG reg2 = INS_OperandReg(ins, 1);
             if(INS_OperandIsMemory(ins, 2))
             {
                 INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)vmulps_regmem, IARG_REG_REFERENCE, reg1, IARG_REG_REFERENCE, reg2, IARG_MEMORYREAD_EA , IARG_MEMORYREAD_SIZE, IARG_END);
                 INS_Delete(ins);
             }
             else
             {
                 REG reg3 = INS_OperandReg(ins, 2);
                 INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)vmulps_regreg, IARG_REG_REFERENCE, reg1, IARG_REG_REFERENCE, reg2, IARG_REG_REFERENCE, reg3,  IARG_END);
                 INS_Delete(ins);
             }
             break;              
        } 
        default:
        {
            break;
        }
    }
}

// This function is called when the application exits
VOID Fini(INT32 code, VOID *v)  
{
    // Write to a file since cout and cerr maybe closed by the application
}

/* ===================================================================== */
/* Print Help Message                                                    */
/* ===================================================================== */

INT32 Usage()
{
    cerr << "This tool replaces all multiplications ith fixed-posit multiplications and also logs the operands." << endl;
    cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */
/*   argc, argv are the entire command line: pin -t <toolname> -- ...    */
/* ===================================================================== */

int main(int argc, char * argv[])
{
    
    // Initialize pin
    if (PIN_Init(argc, argv)) return Usage();

    posit_length = KnobBitWidth.Value();
    es           = KnobExponentSize.Value();
    regime_len   = KnobRegimeSize.Value();

    assert(posit_length >= es + regime_len + 1);
    
    useed        = pow(2.0, (double)es);
    frc_len      = posit_length - es - regime_len - 1;

    if(KnobLog)
    {
        logfile  = fopen(KnobOutputFile.Value().c_str(),"w");
    }

    // Register Instruction to be called to instrument instructions
    INS_AddInstrumentFunction(Instruction, 0);

    // Register Fini to be called when the application exits
    PIN_AddFiniFunction(Fini, 0);
    
    // Start the program, never returns
    PIN_StartProgram();

    if(KnobLog)
    {
        fclose(logfile);
    }

    return 0;
}

