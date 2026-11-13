#include <stddef.h>
#include <gsl/gsl_spmatrix.h>

#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *input = fopen(argv[1], "r");
  if (!input) return 3;
  gsl_spmatrix *matrix = gsl_spmatrix_fscanf(input);
  fclose(input);
  if (!matrix) return 4;

  printf("{\"rows\":%zu,\"cols\":%zu,\"nnz\":%zu,\"entry_1_3\":%g}\n",
         matrix->size1, matrix->size2, gsl_spmatrix_nnz(matrix),
         gsl_spmatrix_get(matrix, 0, 2));
  gsl_spmatrix_free(matrix);
  return 0;
}
