#include <raylib.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    SetTraceLogLevel(LOG_NONE);
    Wave wave = LoadWave(argv[1]);
    if (!wave.data || wave.channels != 1 || wave.sampleRate != 8000 ||
        wave.sampleSize != 16 || wave.frameCount < 4) {
        if (wave.data) UnloadWave(wave);
        return 3;
    }
    const int16_t *pcm = (const int16_t *)wave.data;
    int16_t samples[4] = {pcm[0], pcm[1], pcm[2], pcm[3]};
    wav_report(wave.sampleRate, wave.channels, wave.frameCount, samples);
    UnloadWave(wave);
    return 0;
}
