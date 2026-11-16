#include "harness.h"
#include <SFML/Audio/SoundBuffer.hpp>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

bool parse_data(const std::uint8_t *data, std::size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.wav";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return false; }
        offset += static_cast<std::size_t>(n);
    }
    close(fd);
    bool ok = false;
    sf::SoundBuffer buffer;
    if (buffer.loadFromFile(path) && buffer.getChannelCount() == 1 && buffer.getSampleCount() >= 4) {
        const std::int16_t *pcm = buffer.getSamples();
        if (pcm) {
            result->sample_rate = buffer.getSampleRate();
            result->channels = buffer.getChannelCount();
            result->frames = buffer.getSampleCount() / result->channels;
            for (int i = 0; i < 4; ++i) result->first[i] = pcm[i];
            ok = true;
        }
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    Result result{};
    (void)parse_data(data, size, &result);
    return 0;
}
