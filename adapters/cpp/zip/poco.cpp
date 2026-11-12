#include <Poco/Zip/ZipArchive.h>
#include <Poco/Zip/ZipStream.h>
#include "../../c/zip/report.h"
#include <fstream>
#include <iterator>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream input(argv[1], std::ios::binary);
    if (!input) return 1;
    Poco::Zip::ZipArchive archive(input);
    const auto first = archive.headerBegin();
    if (first == archive.headerEnd()) return 1;
    const std::string name = first->second.getFileName();
    input.clear();
    Poco::Zip::ZipInputStream decoded(input, first->second);
    const std::string content(std::istreambuf_iterator<char>{decoded}, {});
    if (!decoded.crcValid()) return 1;
    zip_report(static_cast<size_t>(std::distance(archive.headerBegin(), archive.headerEnd())),
               name.c_str(), reinterpret_cast<const unsigned char *>(content.data()), content.size());
    return 0;
}
