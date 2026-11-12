#define DR_WAV_IMPLEMENTATION
#include <dr_wav.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    drwav wav;
    if (!drwav_init_file(&wav, argv[1], NULL)) return 3;
    int16_t samples[4] = {0};
    if (wav.channels != 1 || wav.sampleRate != 8000 ||
        drwav_read_pcm_frames_s16(&wav, 4, samples) != 4) {
        drwav_uninit(&wav);
        return 4;
    }
    wav_report(wav.sampleRate, wav.channels, wav.totalPCMFrameCount, samples);
    drwav_uninit(&wav);
    return 0;
}
