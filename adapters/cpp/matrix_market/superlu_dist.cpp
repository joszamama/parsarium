#include <superlu_ddefs.h>

#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    FILE *input = std::fopen(argv[1], "rb");
    if (!input) return 2;
    int_t rows = 0, cols = 0, nonzeros = 0;
    double *values = nullptr;
    int_t *row_ids = nullptr, *col_ptrs = nullptr;
    dreadMM_dist(input, &rows, &cols, &nonzeros, &values, &row_ids, &col_ptrs);
    std::fclose(input);
    if (!values || !row_ids || !col_ptrs) return 3;
    double entry = 0;
    bool found = false;
    for (int_t i = col_ptrs[2]; i < col_ptrs[3]; i++) {
        if (row_ids[i] == 2) {
            entry = values[i];
            found = true;
        }
    }
    if (!found) return 4;
    std::printf("{\"rows\":%lld,\"cols\":%lld,\"nnz\":%lld,\"entry_3_3\":%.10g}\n",
                (long long)rows, (long long)cols, (long long)nonzeros, entry);
    SUPERLU_FREE(values);
    SUPERLU_FREE(row_ids);
    SUPERLU_FREE(col_ptrs);
    return 0;
}
