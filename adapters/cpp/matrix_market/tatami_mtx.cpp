#include <tatami_mtx/tatami_mtx.hpp>

#include <cstdio>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    auto matrix = tatami_mtx::load_matrix_from_text_file<double, int>(argv[1], {});
    if (!matrix || !matrix->sparse()) return 2;
    auto row = matrix->dense_row();
    std::vector<double> values(static_cast<size_t>(matrix->ncol()));
    const double *first = row->fetch(0, values.data());
    std::printf("{\"rows\":%d,\"cols\":%d,\"entry_1_3\":%.10g}\n",
                matrix->nrow(), matrix->ncol(), first[2]);
    return 0;
}
