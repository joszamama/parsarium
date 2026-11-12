#include <sndfile.h>
#include <stdint.h>
#include <string.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    SF_INFO info;
    memset(&info, 0, sizeof(info));
    SNDFILE *file = sf_open(argv[1], SFM_READ, &info);
    if (!file) return 3;
    int16_t samples[4] = {0};
    if ((info.format & SF_FORMAT_TYPEMASK) != SF_FORMAT_WAV ||
        info.channels != 1 || info.samplerate != 8000 ||
        sf_readf_short(file, samples, 4) != 4) {
        sf_close(file);
        return 4;
    }
    wav_report((unsigned int)info.samplerate, (unsigned int)info.channels,
               (uint64_t)info.frames, samples);
    sf_close(file);
    return 0;
}
