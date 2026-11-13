#include <igl/readPLY.h>
#include <Eigen/Core>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  Eigen::MatrixXd vertices;
  Eigen::MatrixXi faces;
  if (!igl::readPLY(argv[1], vertices, faces)) return 1;
  if (vertices.cols() != 3 || faces.cols() != 3) return 1;
  std::printf("{\"vertices\":%ld,\"faces\":%ld,\"face\":[%d,%d,%d]}\n",
              static_cast<long>(vertices.rows()), static_cast<long>(faces.rows()),
              faces(0, 0), faces(0, 1), faces(0, 2));
  return 0;
}
