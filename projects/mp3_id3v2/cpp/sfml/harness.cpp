#include "harness.h"
#include <SFML/Audio/InputSoundFile.hpp>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

bool parse_data(const std::uint8_t *data, std::size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp3";
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
    sf::InputSoundFile file;
    if (file.openFromFile(path)) {
        std::int16_t sample = 0;
        result->decoded_samples = static_cast<unsigned>(file.read(&sample, 1));
        result->samples = file.getSampleCount();
        result->sample_rate = file.getSampleRate();
        result->channels = file.getChannelCount();
        ok = result->decoded_samples == 1 && result->samples > 0;
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    Result result{};
    (void)parse_data(data, size, &result);
    return 0;
}
