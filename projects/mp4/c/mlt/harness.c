#define _GNU_SOURCE
#include "harness.h"
#include <framework/mlt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void copy_codec(char out[64], const char *name) {
    if (!name) return;
    size_t length = strlen(name);
    if (length && length < 64) memcpy(out, name, length + 1);
}

int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-mlt-XXXXXX.mp4";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    if (close(fd)) { unlink(path); return 0; }
    mlt_repository repository = mlt_factory_init(NULL);
    if (!repository) { unlink(path); return 0; }
    mlt_profile profile = mlt_profile_init(NULL);
    if (!profile) { mlt_factory_close(); unlink(path); return 0; }
    mlt_producer producer = mlt_factory_producer(profile, "avformat", path);
    unlink(path);
    if (!producer) { mlt_profile_close(profile); mlt_factory_close(); return 0; }
    mlt_properties properties = mlt_producer_properties(producer);
    result->streams = mlt_properties_get_int(properties, "meta.media.nb_streams");
    /* Stream count, codecs and the first video stream's size are the
       producer's meta.media properties; a missing stream kind stays unset. */
    int ok = result->streams >= 0;
    if (ok) {
        for (int i = 0; i < result->streams; ++i) {
            char key[96];
            snprintf(key, sizeof(key), "meta.media.%d.stream.type", i);
            const char *type = mlt_properties_get(properties, key);
            snprintf(key, sizeof(key), "meta.media.%d.codec.name", i);
            const char *codec = mlt_properties_get(properties, key);
            if (type && strcmp(type, "video") == 0 && !result->has_video) {
                result->has_video = 1;
                copy_codec(result->video_codec, codec);
                snprintf(key, sizeof(key), "meta.media.%d.codec.width", i);
                result->width = mlt_properties_get_int(properties, key);
                snprintf(key, sizeof(key), "meta.media.%d.codec.height", i);
                result->height = mlt_properties_get_int(properties, key);
            } else if (type && strcmp(type, "audio") == 0 && !result->has_audio) {
                result->has_audio = 1;
                copy_codec(result->audio_codec, codec);
            }
        }
    }
    mlt_producer_close(producer);
    mlt_profile_close(profile);
    mlt_factory_close();
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp4_result result;
    (void)parsarium_parse_mp4(data, size, &result);
    return 0;
}
