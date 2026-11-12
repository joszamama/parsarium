#define ALLEGRO_NO_MAGIC_MAIN
#include <allegro5/allegro.h>
#include <allegro5/allegro_audio.h>
#include <allegro5/allegro_acodec.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!al_init() || !al_install_audio() || !al_init_acodec_addon()) return 3;
    ALLEGRO_SAMPLE *sample = al_load_sample(argv[1]);
    if (!sample) return 4;
    if (al_get_sample_depth(sample) != ALLEGRO_AUDIO_DEPTH_INT16 ||
        al_get_sample_channels(sample) != ALLEGRO_CHANNEL_CONF_1 ||
        al_get_sample_length(sample) < 4) return 5;
    const int16_t *pcm = (const int16_t *)al_get_sample_data(sample);
    if (!pcm) return 6;
    int16_t samples[4] = {pcm[0], pcm[1], pcm[2], pcm[3]};
    wav_report(al_get_sample_frequency(sample), 1, al_get_sample_length(sample), samples);
    al_destroy_sample(sample);
    al_uninstall_system();
    return 0;
}
