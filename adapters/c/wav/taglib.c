#include <taglib/tag_c.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    TagLib_File *file = taglib_file_new_type(argv[1], TagLib_File_WAV);
    if (!file || !taglib_file_is_valid(file)) return 3;
    const TagLib_AudioProperties *audio = taglib_file_audioproperties(file);
    if (!audio) return 4;
    printf("{\"sample_rate\":%d,\"channels\":%d,\"bitrate_kbps\":%d}\n",
           taglib_audioproperties_samplerate(audio),
           taglib_audioproperties_channels(audio),
           taglib_audioproperties_bitrate(audio));
    taglib_file_free(file);
    return 0;
}
