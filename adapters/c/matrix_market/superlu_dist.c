#include <superlu_ddefs.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    FILE *input = fopen(argv[1], "rb");
    if (!input) return 2;
    int_t rows = 0, cols = 0, nonzeros = 0;
    double *values = NULL;
    int_t *row_ids = NULL, *col_ptrs = NULL;
    dreadMM_dist(input, &rows, &cols, &nonzeros, &values, &row_ids, &col_ptrs);
    fclose(input);
    if (!values || !row_ids || !col_ptrs) return 3;
    double entry = 0;
    int found = 0;
    for (int_t i = col_ptrs[2]; i < col_ptrs[3]; i++) {
        if (row_ids[i] == 2) {
            entry = values[i];
            found = 1;
        }
    }
    if (!found) return 4;
    printf("{\"rows\":%lld,\"cols\":%lld,\"nnz\":%lld,\"entry_3_3\":%.10g}\n",
           (long long)rows, (long long)cols, (long long)nonzeros, entry);
    SUPERLU_FREE(values);
    SUPERLU_FREE(row_ids);
    SUPERLU_FREE(col_ptrs);
    return 0;
}
