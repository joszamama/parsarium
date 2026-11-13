#include <unsupported/Eigen/SparseExtra>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  Eigen::SparseMatrix<double> matrix;
  if (!Eigen::loadMarket(matrix, argv[1])) return 1;
  std::printf("{\"rows\":%ld,\"cols\":%ld,\"nnz\":%ld,\"entry_1_3\":%.1f}\n",
              static_cast<long>(matrix.rows()), static_cast<long>(matrix.cols()),
              static_cast<long>(matrix.nonZeros()),
              matrix.coeff(0, 2));
  return 0;
}
