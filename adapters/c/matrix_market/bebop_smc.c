#include <bebop/util/init.h>
#include <bebop/smc/coo_matrix.h>
#include <bebop/smc/read_mm.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int initialized = 0;
    bebop_default_initialize(argc, argv, &initialized);
    struct coo_matrix_t matrix = {0};
    if (read_matrix_market_sparse(argv[1], &matrix) != 0) return 1;
    double entry = 0;
    for (int i = 0; i < matrix.nnz; i++) {
        if (matrix.II[i] == 0 && matrix.JJ[i] == 2)
            entry = ((double *)matrix.val)[i];
    }
    printf("{\"rows\":%d,\"cols\":%d,\"nnz\":%d,\"entry_1_3\":%.1f}\n",
           matrix.m, matrix.n, matrix.nnz, entry);
    dealloc_coo_matrix(&matrix);
    return 0;
}
