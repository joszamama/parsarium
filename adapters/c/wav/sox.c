#include <sox.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (sox_init() != SOX_SUCCESS) return 3;
    sox_format_t *file = sox_open_read(argv[1], NULL, NULL, NULL);
    if (!file) return 4;
    sox_sample_t raw[4] = {0};
    if (file->signal.channels != 1 || (unsigned int)file->signal.rate != 8000 ||
        sox_read(file, raw, 4) != 4) return 5;
    sox_uint64_t clips = 0;
    SOX_SAMPLE_LOCALS;
    int16_t samples[4];
    for (int i = 0; i < 4; i++)
        samples[i] = SOX_SAMPLE_TO_SIGNED_16BIT(raw[i], clips);
    wav_report((unsigned int)file->signal.rate, file->signal.channels,
               file->signal.length / file->signal.channels, samples);
    sox_close(file);
    sox_quit();
    return 0;
}
