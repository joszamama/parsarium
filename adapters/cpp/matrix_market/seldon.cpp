#include "SeldonLib.hxx"

#include <iostream>

int main(int argc, char** argv) {
  if (argc != 2) return 2;

  Seldon::Matrix<double, Seldon::General, Seldon::ArrayRowSparse> matrix;
  Seldon::ReadMatrixMarket(argv[1], matrix);

  std::cout << "{\"rows\":" << matrix.GetM()
            << ",\"cols\":" << matrix.GetN()
            << ",\"entry_1_1\":" << matrix(0, 0)
            << ",\"entry_1_3\":" << matrix(0, 2)
            << ",\"entry_2_2\":" << matrix(1, 1) << "}\n";
}
