#include <rsb.h>

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2 || rsb_lib_init(RSB_NULL_INIT_OPTIONS) != RSB_ERR_NO_ERROR) return 1;
    rsb_err_t error = RSB_ERR_NO_ERROR;
    struct rsb_mtx_t *matrix = rsb_file_mtx_load(
        argv[1], RSB_FLAG_NOFLAGS, RSB_NUMERICAL_TYPE_DOUBLE, &error);
    if (!matrix || error != RSB_ERR_NO_ERROR) return 2;
    rsb_coo_idx_t rows = 0, cols = 0;
    rsb_nnz_idx_t nonzeros = 0;
    if (rsb_mtx_get_info(matrix, RSB_MIF_MATRIX_ROWS__TO__RSB_COO_INDEX_T, &rows) ||
        rsb_mtx_get_info(matrix, RSB_MIF_MATRIX_COLS__TO__RSB_COO_INDEX_T, &cols) ||
        rsb_mtx_get_info(matrix, RSB_MIF_MATRIX_NNZ__TO__RSB_NNZ_INDEX_T, &nonzeros)) return 3;
    double *values = calloc((size_t)nonzeros, sizeof(*values));
    rsb_coo_idx_t *row_ids = calloc((size_t)nonzeros, sizeof(*row_ids));
    rsb_coo_idx_t *col_ids = calloc((size_t)nonzeros, sizeof(*col_ids));
    if (!values || !row_ids || !col_ids ||
        rsb_mtx_get_coo(matrix, values, row_ids, col_ids, RSB_FLAG_NOFLAGS)) return 4;
    double entry = 0;
    int found = 0;
    for (rsb_nnz_idx_t i = 0; i < nonzeros; i++) {
        if (row_ids[i] == 0 && col_ids[i] == 2) {
            entry = values[i];
            found = 1;
        }
    }
    if (!found) return 5;
    printf("{\"rows\":%lld,\"cols\":%lld,\"nnz\":%lld,\"entry_1_3\":%.10g}\n",
           (long long)rows, (long long)cols, (long long)nonzeros, entry);
    free(values);
    free(row_ids);
    free(col_ids);
    rsb_mtx_free(matrix);
    return rsb_lib_exit(RSB_NULL_EXIT_OPTIONS) == RSB_ERR_NO_ERROR ? 0 : 6;
}
