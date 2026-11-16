#include "harness.h"
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <id3.h>
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
    ID3Tag *tag = ID3Tag_New();
    int ok = 0;
    if (tag && ID3Tag_LinkWithFlags(tag, path, ID3TT_ID3V2) != 0) {
        ID3Frame *frame = ID3Tag_FindFrameWithID(tag, ID3FID_TITLE);
        ID3Field *field = frame ? ID3Frame_GetField(frame, ID3FN_TEXT) : NULL;
        if (field && ID3Field_GetASCII(field, result->title, sizeof(result->title)) > 0) {
            result->frames = ID3Tag_NumFrames(tag);
            ok = result->frames > 0;
        }
    }
    if (tag) ID3Tag_Delete(tag);
    unlink(path);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
