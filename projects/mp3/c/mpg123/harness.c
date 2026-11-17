#include "harness.h"
#include <mpg123.h>
#include <string.h>
/* Feed the whole byte buffer to libmpg123 and decode every MPEG audio frame. */
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    int err = MPG123_OK;
    mpg123_handle *mh = mpg123_new(NULL, &err);
    if (!mh) return 0;
    mpg123_param2(mh, MPG123_ADD_FLAGS, MPG123_QUIET, 0);
    int ok = mpg123_open_feed(mh) == MPG123_OK && mpg123_feed(mh, data, size) == MPG123_OK;
    long rate = 0; int channels = 0, encoding = 0, layer = 0;
    while (ok) {
        off_t num; unsigned char *audio; size_t bytes;
        int ret = mpg123_decode_frame(mh, &num, &audio, &bytes);
        if (ret == MPG123_NEW_FORMAT) {
            ok = mpg123_getformat(mh, &rate, &channels, &encoding) == MPG123_OK;
            continue;
        }
        if (ret == MPG123_NEED_MORE || ret == MPG123_DONE) break;
        if (ret != MPG123_OK) { ok = 0; break; }
        struct mpg123_frameinfo2 info;
        if (mpg123_info2(mh, &info) != MPG123_OK) { ok = 0; break; }
        if (layer && (unsigned)info.layer != (unsigned)layer) { ok = 0; break; }
        layer = info.layer;
        result->frames++;
        if (channels > 0 && encoding) result->decoded_samples += (unsigned)(bytes / ((size_t)channels * (size_t)mpg123_encsize(encoding)));
    }
    ok = ok && result->frames > 0 && rate > 0 && channels > 0;
    if (ok) { result->sample_rate = (unsigned)rate; result->channels = (unsigned)channels; result->layer = (unsigned)layer; }
    mpg123_close(mh);
    mpg123_delete(mh);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result; (void)parsarium_parse_mp3(data, size, &result); return 0;
}
