#include "pnm.hpp"
#include <cstdio>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    try {
        const pnm::image<pnm::rgb_pixel> image = pnm::read(argv[1]);
        if (image.width() != 2 || image.height() != 1) return 1;
        const auto first = image[0][0];
        const auto second = image[0][1];
        std::printf("{\"width\":%zu,\"height\":%zu,\"first\":[%u,%u,%u,255],"
                    "\"second\":[%u,%u,%u,255]}\n",
                    image.width(), image.height(),
                    first.red, first.green, first.blue,
                    second.red, second.green, second.blue);
        return 0;
    } catch (const std::exception&) {
        return 1;
    }
}
