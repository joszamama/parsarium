#include <viennacl/io/matrix_market.hpp>
#include <viennacl/tools/adapter.hpp>

#include <iostream>
#include <map>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    std::vector<std::map<unsigned int, double>> values;
    viennacl::tools::sparse_matrix_adapter<double> matrix(values);
    if (!viennacl::io::read_matrix_market_file(matrix, argv[1])) return 2;
    std::size_t nonzero = 0;
    for (const auto &row : values) nonzero += row.size();
    if (matrix.size1() < 1 || matrix.size2() < 3) return 3;
    const auto entry = values.at(0).find(2);
    if (entry == values.at(0).end()) return 4;
    std::cout << "{\"rows\":" << matrix.size1()
              << ",\"cols\":" << matrix.size2()
              << ",\"nnz\":" << nonzero
              << ",\"entry_1_3\":" << entry->second << "}\n";
}
