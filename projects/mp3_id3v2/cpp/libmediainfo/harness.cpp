#include "harness.h"
#include <MediaInfo/MediaInfo.h>
#include <cstdlib>
#include <cstring>
#include <string>
#include <unistd.h>

static int copy_ascii(char *out, size_t capacity, const std::wstring &input) {
    if (input.empty() || input.size() >= capacity) return 0;
    for (size_t i = 0; i < input.size(); i++) {
        wchar_t ch = input[i];
        if (ch < 32 || ch > 126 || ch == L'"' || ch == L'\\') return 0;
        out[i] = static_cast<char>(ch);
    }
    out[input.size()] = 0;
    return 1;
}
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp3";
    int fd = mkstemps(path, 4); if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += static_cast<size_t>(n);
    }
    close(fd);
    MediaInfoLib::MediaInfo info;
    const std::wstring wide_path(path, path + std::strlen(path));
    int ok = info.Open(wide_path) != 0;
    if (ok) {
        ok = copy_ascii(result->title, sizeof(result->title), info.Get(MediaInfoLib::Stream_General, 0, L"Title")) &&
             copy_ascii(result->format, sizeof(result->format), info.Get(MediaInfoLib::Stream_Audio, 0, L"Format"));
        try { result->sample_rate = std::stoi(static_cast<std::wstring>(info.Get(MediaInfoLib::Stream_Audio, 0, L"SamplingRate"))); }
        catch (...) { ok = 0; }
        ok = ok && result->sample_rate > 0;
    }
    info.Close();
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result;
    (void)parsarium_parse_mp3(data, size, &result);
    return 0;
}
