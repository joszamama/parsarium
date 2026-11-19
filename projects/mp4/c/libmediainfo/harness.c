#include "harness.h"
#include <MediaInfoDLL/MediaInfoDLL_Static.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* MediaInfo returns "" for a field the input does not have; that field is
   left NULL and omitted from the output. */
static int copy_field(char **out, void *handle, MediaInfo_stream_C stream, const char *name) {
    const char *value = MediaInfoA_Get(handle, stream, 0, name, MediaInfo_Info_Text, MediaInfo_Info_Name);
    if (!value || !*value) return 1;
    *out = strdup(value);
    return *out != NULL;
}

int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp4";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    void *handle = MediaInfoA_New();
    int ok = handle && MediaInfoA_Open(handle, path);
    if (ok) {
        ok = copy_field(&result->container, handle, MediaInfo_Stream_General, "Format") &&
             copy_field(&result->title, handle, MediaInfo_Stream_General, "Title") &&
             copy_field(&result->video, handle, MediaInfo_Stream_Video, "Format") &&
             copy_field(&result->audio, handle, MediaInfo_Stream_Audio, "Format") &&
             copy_field(&result->width, handle, MediaInfo_Stream_Video, "Width") &&
             copy_field(&result->height, handle, MediaInfo_Stream_Video, "Height");
        MediaInfoA_Close(handle);
        if (!ok) parsarium_free_mp4(result);
    }
    if (handle) MediaInfoA_Delete(handle);
    unlink(path);
    return ok;
}

void parsarium_free_mp4(struct parsarium_mp4_result *result) {
    free(result->container); free(result->title); free(result->video);
    free(result->audio); free(result->width); free(result->height);
    memset(result, 0, sizeof(*result));
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp4_result result;
    if (parsarium_parse_mp4(data, size, &result)) parsarium_free_mp4(&result);
    return 0;
}
