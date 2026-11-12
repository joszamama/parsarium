#include <bit7z/bitarchivereader.hpp>
#include "../../c/zip/report.h"
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    bit7z::Bit7zLibrary library{
        "/opt/homebrew/Cellar/sevenzip/26.04/lib/7z.so"};
    bit7z::BitArchiveReader archive{library, argv[1], bit7z::BitFormat::Zip};
    if (archive.itemsCount() == 0) return 1;
    const std::string name = archive.itemAt(0).name();
    bit7z::buffer_t content;
    archive.extractTo(content, 0);
    zip_report(archive.itemsCount(), name.c_str(), content.data(), content.size());
    return 0;
}
