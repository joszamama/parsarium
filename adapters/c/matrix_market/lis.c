#include <lis.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (lis_initialize(&argc, &argv) != LIS_SUCCESS) return 1;
  LIS_MATRIX matrix;
  if (lis_matrix_create(LIS_COMM_WORLD, &matrix) != LIS_SUCCESS) return 1;
  if (lis_input_matrix(matrix, argv[1]) != LIS_SUCCESS) return 1;
  LIS_INT local_rows = 0, rows = 0, nnz = 0;
  if (lis_matrix_get_size(matrix, &local_rows, &rows) != LIS_SUCCESS) return 1;
  if (lis_matrix_get_nnz(matrix, &nnz) != LIS_SUCCESS) return 1;
  printf("{\"rows\":%ld,\"nnz\":%ld}\n", (long) rows, (long) nnz);
  lis_matrix_destroy(matrix);
  lis_finalize();
  return 0;
}
