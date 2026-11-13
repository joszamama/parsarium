#include "Teuchos_MatrixMarket_Raw_Reader.hpp"

#include <iostream>

int main(int argc, char** argv) {
  if (argc != 2) return 2;

  Teuchos::MatrixMarket::Raw::Reader<double, int> reader;
  Teuchos::ArrayRCP<int> rowptr, colind;
  Teuchos::ArrayRCP<double> values;
  int rows = 0;
  int cols = 0;
  const bool parsed = reader.readFile(rowptr, colind, values, rows, cols, argv[1]);

  double entry_1_3 = 0;
  for (int i = rowptr[0]; i < rowptr[1]; ++i) {
    if (colind[i] == 2) entry_1_3 = values[i];
  }
  std::cout << "{\"parsed\":" << (parsed ? "true" : "false")
            << ",\"rows\":" << rows << ",\"cols\":" << cols
            << ",\"nnz\":" << values.size()
            << ",\"entry_1_3\":" << entry_1_3 << "}\n";
}
