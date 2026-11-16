#include "harness.h"
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <id3/tag.h>
#include <id3/id3lib_frame.h>
#include <id3/field.h>
int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp3";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    ID3_Tag tag;
    int ok = 0;
    if (tag.Link(path, ID3TT_ID3V2) != 0) {
        ID3_Frame *frame = tag.Find(ID3FID_TITLE);
        ID3_Field *field = frame ? frame->GetField(ID3FN_TEXT) : nullptr;
        if (field && field->Get(result->title, sizeof(result->title)) > 0) {
            result->frames = tag.NumFrames();
            ok = result->frames > 0;
        }
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
