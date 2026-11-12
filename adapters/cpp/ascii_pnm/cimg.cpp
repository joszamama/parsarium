#define cimg_display 0
#include "CImg.h"
#include <cstdio>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    try {
        const auto image = cimg_library::CImg<unsigned char>::get_load_pnm(argv[1]);
        if (image.width() != 2 || image.height() != 1 || image.spectrum() != 3)
            return 1;
        std::printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,255],"
                    "\"second\":[%u,%u,%u,255]}\n",
                    image.width(), image.height(),
                    image(0, 0, 0, 0), image(0, 0, 0, 1), image(0, 0, 0, 2),
                    image(1, 0, 0, 0), image(1, 0, 0, 1), image(1, 0, 0, 2));
        return 0;
    } catch (const cimg_library::CImgException&) {
        return 1;
    }
}
