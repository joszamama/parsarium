#include <AudioFile.h>
#include "harness.h"
#include <vector>

int parsarium_parse_wav(const uint8_t *data, size_t size,
                        struct parsarium_wav_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    AudioFile<int16_t> audio;
    std::vector<uint8_t> bytes(data, data + size);
    if (!audio.loadFromMemory(bytes)) return 0;
    if (audio.getNumChannels() != 1 || audio.getNumSamplesPerChannel() < 4) return 0;
    const auto &pcm = audio.samples[0];
    result->sample_rate = audio.getSampleRate();
    result->channels = audio.getNumChannels();
    result->frames = audio.getNumSamplesPerChannel();
    for (int i = 0; i < 4; ++i) result->samples[i] = pcm[i];
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result;
    (void)parsarium_parse_wav(data, size, &result);
    return 0;
}
