#include <cholmod.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "rb");
  if (!file) return 1;
  cholmod_common common;
  if (!cholmod_l_start(&common)) return 1;
  cholmod_sparse *matrix = cholmod_l_read_sparse2(file, CHOLMOD_DOUBLE, &common);
  fclose(file);
  if (!matrix) {
    cholmod_l_finish(&common);
    return 1;
  }
  long rows = (long) matrix->nrow;
  long cols = (long) matrix->ncol;
  long nnz = (long) cholmod_l_nnz(matrix, &common);
  printf("{\"rows\":%ld,\"cols\":%ld,\"nnz\":%ld}\n", rows, cols, nnz);
  cholmod_l_free_sparse(&matrix, &common);
  cholmod_l_finish(&common);
  return 0;
}
