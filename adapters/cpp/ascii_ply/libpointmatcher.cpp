#include <pointmatcher/IO.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    const auto cloud = PointMatcherIO<double>::loadPLY(argv[1]);
    if (cloud.features.rows() < 3) return 3;
    double x_sum = 0.0;
    double y_sum = 0.0;
    double z_sum = 0.0;
    for (Eigen::Index i = 0; i < cloud.features.cols(); ++i) {
        x_sum += cloud.features(0, i);
        y_sum += cloud.features(1, i);
        z_sum += cloud.features(2, i);
    }
    std::cout << "{\"points\":" << cloud.features.cols()
              << ",\"x_sum\":" << x_sum << ",\"y_sum\":" << y_sum
              << ",\"z_sum\":" << z_sum << "}\n";
}
