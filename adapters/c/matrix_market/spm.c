#include <spm.h>
#include <stdio.h>

int main(int argc, char **argv) {
    spmatrix_t matrix;
    int found = 0;
    double value = 0.0;

    if (argc != 2 || spmReadDriver(SpmDriverMM, argv[1], &matrix) != SPM_SUCCESS) {
        return 2;
    }
    if (matrix.fmttype != SpmIJV || matrix.flttype != SpmDouble) {
        spmExit(&matrix);
        return 3;
    }
    const double *values = (const double *)matrix.values;
    for (spm_int_t i = 0; i < matrix.gnnz; ++i) {
        if (matrix.rowptr[i] == 3 && matrix.colptr[i] == 3) {
            value = values[i];
            found = 1;
        }
    }
    if (!found) {
        spmExit(&matrix);
        return 4;
    }
    printf("{\"rows\":%ld,\"cols\":%ld,\"nnz\":%ld,\"entry_3_3\":%.1f}\n",
           (long)matrix.gN, (long)matrix.gN, (long)matrix.gnnz, value);
    spmExit(&matrix);
    return 0;
}
