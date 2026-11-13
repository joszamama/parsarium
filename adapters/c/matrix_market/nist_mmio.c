#include <stdio.h>
#include <stdlib.h>
#include "mmio.h"

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "r");
  if (!file) return 3;
  MM_typecode type;
  if (mm_read_banner(file, &type)) return 4;
  if (!mm_is_matrix(type) || !mm_is_coordinate(type) ||
      !mm_is_real(type) || !mm_is_general(type)) return 5;
  int rows = 0, columns = 0, entries = 0;
  if (mm_read_mtx_crd_size(file, &rows, &columns, &entries) || entries < 0) return 6;
  int *row = calloc((size_t)entries, sizeof(*row));
  int *column = calloc((size_t)entries, sizeof(*column));
  double *value = calloc((size_t)entries, sizeof(*value));
  if (!row || !column || !value) return 7;
  if (mm_read_mtx_crd_data(file, rows, columns, entries, row, column, value, type)) return 8;
  double selected = 0;
  for (int index = 0; index < entries; index++) {
    if (row[index] == 1 && column[index] == 3) selected = value[index];
  }
  printf("{\"rows\":%d,\"cols\":%d,\"entries\":%d,\"value_1_3\":%.1f}\n",
         rows, columns, entries, selected);
  free(value);
  free(column);
  free(row);
  fclose(file);
  return 0;
}
