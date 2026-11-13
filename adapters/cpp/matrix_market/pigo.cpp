#include <pigo.hpp>

#include <cstdio>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    using Matrix = pigo::WCOO<int, int, std::vector<int>, double, std::vector<double>>;
    Matrix matrix{argv[1], pigo::MATRIX_MARKET};
    double entry = 0;
    bool found = false;
    for (int i = 0; i < matrix.m(); i++) {
        if (matrix.x()[i] == 1 && matrix.y()[i] == 3) {
            entry = matrix.w()[i];
            found = true;
        }
    }
    if (!found) return 2;
    std::printf("{\"reported_rows\":%d,\"reported_cols\":%d,\"nnz\":%d,\"entry_1_3\":%.10g}\n",
                matrix.nrows(), matrix.ncols(), matrix.m(), entry);
    matrix.free();
    return 0;
}
