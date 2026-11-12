#include <audiofile.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    AFfilehandle file = afOpenFile(argv[1], "r", NULL);
    if (!file) return 3;
    if (afGetFileFormat(file, NULL) != AF_FILE_WAVE ||
        afSetVirtualSampleFormat(file, AF_DEFAULT_TRACK, AF_SAMPFMT_TWOSCOMP, 16) != 0) {
        afCloseFile(file);
        return 4;
    }
    int16_t samples[4] = {0};
    if (afReadFrames(file, AF_DEFAULT_TRACK, samples, 4) != 4) {
        afCloseFile(file);
        return 5;
    }
    wav_report((unsigned int)afGetRate(file, AF_DEFAULT_TRACK),
               (unsigned int)afGetChannels(file, AF_DEFAULT_TRACK),
               (uint64_t)afGetFrameCount(file, AF_DEFAULT_TRACK), samples);
    afCloseFile(file);
    return 0;
}
