#include <cstddef>
#include <gsl/gsl_spmatrix.h>

#include <cstdio>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  std::FILE *input = std::fopen(argv[1], "r");
  if (!input) return 3;
  gsl_spmatrix *matrix = gsl_spmatrix_fscanf(input);
  std::fclose(input);
  if (!matrix) return 4;

  std::cout << "{\"rows\":" << matrix->size1
            << ",\"cols\":" << matrix->size2
            << ",\"nnz\":" << gsl_spmatrix_nnz(matrix)
            << ",\"entry_1_3\":" << gsl_spmatrix_get(matrix, 0, 2)
            << "}\n";
  gsl_spmatrix_free(matrix);
}
