#include <OpenImageIO/imageio.h>

#include <cstdint>
#include <iostream>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    auto input = OIIO::ImageInput::open(argv[1]);
    if (!input) return 3;
    const auto& spec = input->spec();
    if (spec.width < 2 || spec.height < 1 || spec.nchannels != 4) return 4;
    std::vector<std::uint8_t> pixels(spec.width * spec.height * spec.nchannels);
    if (!input->read_image(0, 0, 0, spec.nchannels, OIIO::TypeDesc::UINT8, pixels.data())) return 5;
    input->close();
    std::cout << "{\"width\":" << spec.width << ",\"height\":" << spec.height
              << ",\"first\":[" << +pixels[0] << ',' << +pixels[1] << ',' << +pixels[2] << ',' << +pixels[3]
              << "],\"second\":[" << +pixels[4] << ',' << +pixels[5] << ',' << +pixels[6] << ',' << +pixels[7]
              << "]}\n";
}
