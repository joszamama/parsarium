#include <SFML/Audio/SoundBuffer.hpp>
#include <cstdint>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    sf::SoundBuffer buffer;
    if (!buffer.loadFromFile(argv[1]) || buffer.getSampleCount() != 4 ||
        buffer.getChannelCount() != 1) return 3;
    const std::int16_t *samples = buffer.getSamples();
    if (!samples) return 4;
    std::printf("{\"sample_rate\":%u,\"channels\":%u,\"frames\":%llu,\"samples\":[%d,%d,%d,%d]}\n",
                buffer.getSampleRate(), buffer.getChannelCount(),
                static_cast<unsigned long long>(buffer.getSampleCount() / buffer.getChannelCount()),
                samples[0], samples[1], samples[2], samples[3]);
    return 0;
}
