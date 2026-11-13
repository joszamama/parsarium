#include "rplycpp.hpp"

#include <iostream>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 2) return 2;

    rplycpp::PLYReader reader;
    if (!reader.Open(argv[1])) return 3;

    unsigned vertices = 0;
    unsigned faces = 0;
    std::vector<unsigned> face;
    std::vector<rplycpp::PLYReadHandler> handlers;
    for (const auto& element : reader.GetElements()) {
        if (element.GetName() == "vertex") {
            handlers.emplace_back([&](const std::vector<double>& values) {
                if (values.size() >= 3) ++vertices;
            });
        } else if (element.GetName() == "face") {
            handlers.emplace_back([&](const std::vector<double>& values) {
                if (values.size() == 4 && values[0] == 3) {
                    ++faces;
                    face = {static_cast<unsigned>(values[1]),
                            static_cast<unsigned>(values[2]),
                            static_cast<unsigned>(values[3])};
                }
            });
        } else {
            handlers.emplace_back(rplycpp::DEFAULT_HANDLER);
        }
    }
    if (!reader.Read(handlers) || !reader.Close()) return 4;
    if (face.size() != 3) return 5;
    std::cout << "{\"vertices\":" << vertices << ",\"faces\":" << faces
              << ",\"face\":[" << face[0] << ',' << face[1] << ',' << face[2]
              << "]}\n";
}
