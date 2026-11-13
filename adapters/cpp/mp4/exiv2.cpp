#include <exiv2/exiv2.hpp>
#include <cstdio>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    auto image = Exiv2::ImageFactory::open(argv[1]);
    if (!image.get()) return 1;
    image->readMetadata();
    const auto &xmp = image->xmpData();
    auto brand = xmp.findKey(Exiv2::XmpKey("Xmp.video.MajorBrand"));
    auto width = xmp.findKey(Exiv2::XmpKey("Xmp.video.Width"));
    auto height = xmp.findKey(Exiv2::XmpKey("Xmp.video.Height"));
    if (brand == xmp.end() || width == xmp.end() || height == xmp.end()) return 1;
    int w = std::stoi(width->toString());
    int h = std::stoi(height->toString());
    if (brand->toString().find("MP4 Base Media") == std::string::npos) return 1;
    std::printf("{\"brand\":\"MP4 Base Media\",\"width\":%d,\"height\":%d}\n", w, h);
    return 0;
}
