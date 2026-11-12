#include <OpenImageIO/imageio.h>
#include <cstdio>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    auto image = OIIO::ImageInput::open(argv[1]);
    if (!image || image->format_name() != std::string("pnm")) return 1;
    const OIIO::ImageSpec& spec = image->spec();
    if (spec.width != 2 || spec.height != 1 || spec.nchannels != 3) return 1;
    if (spec.get_int_attribute("pnm:binary", -1) != 0) return 1;
    std::vector<unsigned char> pixels(spec.width * spec.height * spec.nchannels);
    if (!image->read_image(0, 0, 0, spec.nchannels,
                           OIIO::span<unsigned char>(pixels.data(), pixels.size()))) return 1;
    std::printf("{\"width\":%d,\"height\":%d,\"format\":\"%s\","
                "\"binary\":0,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
                spec.width, spec.height, image->format_name(),
                pixels[0], pixels[1], pixels[2], pixels[3], pixels[4], pixels[5]);
    return 0;
}
