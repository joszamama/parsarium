#include "hif/utils/io.hpp"

#include <iostream>

int main(int argc, char** argv) {
  if (argc != 2) return 2;

  std::size_t rows = 0;
  std::size_t cols = 0;
  hif::Array<int> row_index, col_index;
  hif::Array<double> values;
  hif::read_mm_sparse(argv[1], rows, cols, row_index, col_index, values);

  double entry_1_3 = 0;
  for (std::size_t i = 0; i < values.size(); ++i) {
    if (row_index[i] == 0 && col_index[i] == 2) entry_1_3 = values[i];
  }
  std::cout << "{\"rows\":" << rows << ",\"cols\":" << cols
            << ",\"nnz\":" << values.size()
            << ",\"entry_1_3\":" << entry_1_3 << "}\n";
}
