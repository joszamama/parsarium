#include <aubio/aubio.h>
#include <math.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    aubio_source_t *source = new_aubio_source(argv[1], 0, 4);
    if (!source) return 3;
    fvec_t *vector = new_fvec(4);
    if (!vector) return 4;
    uint_t read = 0;
    aubio_source_do(source, vector, &read);
    if (read != 4) return 5;
    int16_t samples[4];
    for (int i = 0; i < 4; i++)
        samples[i] = (int16_t)lroundf(vector->data[i] * 32768.0f);
    wav_report(aubio_source_get_samplerate(source), aubio_source_get_channels(source),
               aubio_source_get_duration(source), samples);
    del_fvec(vector);
    del_aubio_source(source);
    return 0;
}
