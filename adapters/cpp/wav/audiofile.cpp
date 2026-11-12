#include "AudioFile.h"
#include <cstdint>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    AudioFile<std::int16_t> audio;
    if (!audio.load(argv[1]) || audio.getNumChannels() != 1 ||
        audio.getNumSamplesPerChannel() != 4) return 3;
    const auto &samples = audio.samples[0];
    std::printf("{\"sample_rate\":%u,\"channels\":%d,\"frames\":%d,\"samples\":[%d,%d,%d,%d]}\n",
                audio.getSampleRate(), audio.getNumChannels(),
                audio.getNumSamplesPerChannel(), samples[0], samples[1], samples[2], samples[3]);
    return 0;
}
