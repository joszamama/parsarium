#include "harness.h"
#include <taglib/tag_c.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.wav";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    TagLib_File *file = taglib_file_new_type(path, TagLib_File_WAV);
    int ok = 0;
    if (file && taglib_file_is_valid(file)) {
        const TagLib_AudioProperties *audio = taglib_file_audioproperties(file);
        if (audio) {
            result->sample_rate = taglib_audioproperties_samplerate(audio);
            result->channels = taglib_audioproperties_channels(audio);
            result->bitrate_kbps = taglib_audioproperties_bitrate(audio);
            ok = result->sample_rate > 0 && result->channels > 0;
        }
    }
    if (file) taglib_file_free(file);
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
