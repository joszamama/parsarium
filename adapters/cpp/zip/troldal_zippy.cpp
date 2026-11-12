#include <Zippy.hpp>
#include "../../c/zip/report.h"
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    Zippy::ZipArchive archive;
    archive.Open(argv[1]);
    const auto names = archive.GetEntryNames();
    if (names.empty()) return 1;
    const std::string content = archive.GetEntry(names[0]).GetDataAsString();
    zip_report(names.size(), names[0].c_str(),
               reinterpret_cast<const unsigned char *>(content.data()), content.size());
    archive.Close();
    return 0;
}
