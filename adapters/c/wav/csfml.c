#include <CSFML/Audio/SoundBuffer.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    sfSoundBuffer *buffer = sfSoundBuffer_createFromFile(argv[1]);
    if (!buffer) return 3;
    unsigned int channels = sfSoundBuffer_getChannelCount(buffer);
    uint64_t sample_count = sfSoundBuffer_getSampleCount(buffer);
    const int16_t *pcm = sfSoundBuffer_getSamples(buffer);
    if (!pcm || channels != 1 || sample_count < 4) return 4;
    int16_t samples[4] = {pcm[0], pcm[1], pcm[2], pcm[3]};
    wav_report(sfSoundBuffer_getSampleRate(buffer), channels,
               sample_count / channels, samples);
    sfSoundBuffer_destroy(buffer);
    return 0;
}
