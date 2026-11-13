#include <libmtx/mtxfile/mtxfile.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct mtxfile matrix;
    int64_t lines = 0, bytes = 0;
    if (mtxfile_read(&matrix, mtx_double, argv[1], false, &lines, &bytes) != 0) return 1;
    double entry = 0.0;
    for (int64_t k = 0; k < matrix.datasize; ++k) {
        const struct mtxfile_matrix_coordinate_real_double *item =
            &matrix.data.matrix_coordinate_real_double[k];
        if (item->i == 1 && item->j == 3) entry = item->a;
    }
    printf("{\"rows\":%" PRId64 ",\"cols\":%" PRId64 ",\"nnz\":%" PRId64 ",\"entry_1_3\":%.1f}\n",
           matrix.size.num_rows, matrix.size.num_columns,
           matrix.size.num_nonzeros, entry);
    mtxfile_free(&matrix);
    return 0;
}
