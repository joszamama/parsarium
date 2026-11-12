#include <zipios/zipfile.hpp>
#include "../../c/zip/report.h"
#include <iterator>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    zipios::ZipFile archive(argv[1]);
    const auto entries = archive.entries();
    if (entries.empty()) return 1;
    const std::string name = entries[0]->getName();
    const auto stream = archive.getInputStream(name);
    if (!stream) return 1;
    const std::string content(std::istreambuf_iterator<char>{*stream}, {});
    zip_report(entries.size(), name.c_str(),
               reinterpret_cast<const unsigned char *>(content.data()), content.size());
    return 0;
}
