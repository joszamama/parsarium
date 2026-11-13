#include <mtl/io/matrix_market.hpp>

#include <iostream>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    const auto matrix = mtl::io::mm_read<double>(argv[1]);
    std::cout << "{\"rows\":" << matrix.num_rows()
              << ",\"cols\":" << matrix.num_cols()
              << ",\"nnz\":" << matrix.nnz()
              << ",\"entry_1_3\":" << matrix(0, 2) << "}\n";
}
