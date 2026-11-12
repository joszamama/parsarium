#include <Zipper/Unzipper.hpp>
#include "../../c/zip/report.h"
#include <sstream>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    zipper::Unzipper archive(argv[1]);
    const auto entries = archive.entries();
    if (entries.empty()) return 1;
    std::stringstream output;
    if (!archive.extract(entries[0].name, output)) return 1;
    const std::string content = output.str();
    zip_report(entries.size(), entries[0].name.c_str(),
               reinterpret_cast<const unsigned char *>(content.data()), content.size());
    archive.close();
    return 0;
}
