#include <fast_matrix_market/fast_matrix_market.hpp>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <vector>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  std::ifstream input(argv[1]);
  if (!input) return 1;
  std::int64_t rows = 0, cols = 0;
  std::vector<std::int64_t> row, col;
  std::vector<double> value;
  fast_matrix_market::read_matrix_market_triplet(input, rows, cols, row, col, value);
  if (value.size() != 3) return 1;
  double entry = 0;
  bool found = false;
  for (std::size_t i = 0; i < value.size(); ++i) {
    if (row[i] == 0 && col[i] == 2) {
      entry = value[i];
      found = true;
    }
  }
  if (!found) return 1;
  std::printf("{\"rows\":%lld,\"cols\":%lld,\"nnz\":%zu,\"entry_1_3\":%.1f}\n",
              static_cast<long long>(rows), static_cast<long long>(cols),
              value.size(), entry);
  return 0;
}
