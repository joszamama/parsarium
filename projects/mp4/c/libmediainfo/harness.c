#include "harness.h"
#include <MediaInfoDLL/MediaInfoDLL_Static.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static int copy_ascii(char *out, size_t capacity, const char *input) {
    if (!input || !*input) return 0;
    size_t length = strlen(input);
    if (length >= capacity) return 0;
    for (size_t i = 0; i < length; i++)
        if ((unsigned char)input[i] < 32 || (unsigned char)input[i] > 126 || input[i] == '"' || input[i] == '\\') return 0;
    memcpy(out, input, length + 1);
    return 1;
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
        ok = copy_ascii(result->container, sizeof(result->container), MediaInfoA_Get(handle, MediaInfo_Stream_General, 0, "Format", MediaInfo_Info_Text, MediaInfo_Info_Name)) &&
             copy_ascii(result->title, sizeof(result->title), MediaInfoA_Get(handle, MediaInfo_Stream_General, 0, "Title", MediaInfo_Info_Text, MediaInfo_Info_Name)) &&
             copy_ascii(result->video, sizeof(result->video), MediaInfoA_Get(handle, MediaInfo_Stream_Video, 0, "Format", MediaInfo_Info_Text, MediaInfo_Info_Name)) &&
             copy_ascii(result->audio, sizeof(result->audio), MediaInfoA_Get(handle, MediaInfo_Stream_Audio, 0, "Format", MediaInfo_Info_Text, MediaInfo_Info_Name));
        result->width = atoi(MediaInfoA_Get(handle, MediaInfo_Stream_Video, 0, "Width", MediaInfo_Info_Text, MediaInfo_Info_Name));
        result->height = atoi(MediaInfoA_Get(handle, MediaInfo_Stream_Video, 0, "Height", MediaInfo_Info_Text, MediaInfo_Info_Name));
        ok = ok && result->width > 0 && result->height > 0;
        MediaInfoA_Close(handle);
    }
    if (handle) MediaInfoA_Delete(handle);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp4_result result;
    (void)parsarium_parse_mp4(data, size, &result);
    return 0;
}
