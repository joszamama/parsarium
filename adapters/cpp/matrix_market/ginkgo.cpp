#include <ginkgo/core/base/mtx_io.hpp>
#include <cstdio>
#include <fstream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  std::ifstream input(argv[1]);
  if (!input) return 1;
  auto matrix = gko::read_raw<double, int>(input);
  double entry = 0;
  bool found = false;
  for (const auto &nz : matrix.nonzeros) {
    if (nz.row == 0 && nz.column == 2) {
      entry = nz.value;
      found = true;
    }
  }
  if (!found) return 1;
  std::printf("{\"rows\":%zu,\"cols\":%zu,\"nnz\":%zu,\"entry_1_3\":%.1f}\n",
              matrix.size[0], matrix.size[1], matrix.nonzeros.size(), entry);
  return 0;
}
