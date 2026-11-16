#include "harness.h"
#include <allegro5/allegro_audio.h>
#include <allegro5/allegro_acodec.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.wav";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    int ok = 0;
    if (al_install_audio() && al_init_acodec_addon()) {
        ALLEGRO_SAMPLE *sample = al_load_sample(path);
        if (sample && al_get_sample_depth(sample) == ALLEGRO_AUDIO_DEPTH_INT16 &&
            al_get_sample_channels(sample) == ALLEGRO_CHANNEL_CONF_1 &&
            al_get_sample_length(sample) >= 4) {
            const int16_t *pcm = (const int16_t *)al_get_sample_data(sample);
            if (pcm) {
                result->sample_rate = al_get_sample_frequency(sample);
                result->channels = 1;
                result->frames = al_get_sample_length(sample);
                memcpy(result->samples, pcm, 8);
                ok = 1;
            }
        }
        if (sample) al_destroy_sample(sample);
        al_uninstall_audio();
    }
    unlink(path);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
