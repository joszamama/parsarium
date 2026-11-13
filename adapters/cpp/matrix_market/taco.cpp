#include "taco/tensor.h"

#include <iostream>

int main(int argc, char** argv) {
  if (argc != 2) return 2;

  taco::Tensor<double> matrix = taco::read(argv[1], taco::Sparse);
  std::size_t nnz = 0;
  double entry_1_3 = 0;
  for (auto it = matrix.begin(); it != matrix.end(); ++it) {
    ++nnz;
    if (it->first[0] == 0 && it->first[1] == 2) entry_1_3 = it->second;
  }
  std::cout << "{\"rows\":" << matrix.getDimension(0)
            << ",\"cols\":" << matrix.getDimension(1)
            << ",\"nnz\":" << nnz
            << ",\"entry_1_3\":" << entry_1_3 << "}\n";
}
