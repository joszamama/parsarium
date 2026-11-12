#include <libzippp.h>
#include "../../c/zip/report.h"
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    libzippp::ZipArchive archive(argv[1]);
    if (!archive.open(libzippp::ZipArchive::ReadOnly)) return 1;
    const auto entries = archive.getEntries();
    if (entries.empty()) { archive.close(); return 1; }
    const std::string name = entries[0].getName();
    const std::string content = entries[0].readAsText();
    zip_report(entries.size(), name.c_str(),
               reinterpret_cast<const unsigned char *>(content.data()), content.size());
    archive.close();
    return 0;
}
