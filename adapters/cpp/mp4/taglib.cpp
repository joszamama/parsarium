#include <taglib/mp4file.h>
#include <taglib/mp4tag.h>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    TagLib::MP4::File file(argv[1]);
    if (!file.isValid() || file.tag() == nullptr || file.audioProperties() == nullptr) return 1;
    std::printf("{\"title\":\"%s\",\"duration_seconds\":%d}\n",
                file.tag()->title().toCString(true), file.audioProperties()->lengthInSeconds());
    return 0;
}
