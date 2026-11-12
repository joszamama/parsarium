#include <zipper/unzipper.h>
#include "../../c/zip/report.h"
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    zipper::Unzipper archive(argv[1]);
    const std::vector<zipper::ZipEntry> entries = archive.entries();
    if (entries.empty()) return 1;
    std::vector<unsigned char> content;
    if (!archive.extractEntryToMemory(entries[0].name, content)) return 1;
    zip_report(entries.size(), entries[0].name.c_str(), content.data(), content.size());
    archive.close();
    return 0;
}
