#include "harness.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    static uint8_t input[1u << 20];
    size_t size = fread(input, 1, sizeof(input), file);
    if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) {
        fclose(file); return 4;
    }
    fclose(file);
    struct parsarium_mp4_result result;
    if (!parsarium_parse_mp4(input, size, &result)) return 5;
    printf("{\"streams\":%d,\"video_codec\":", result.streams);
    if (result.video_codec[0]) printf("\"%s\"", result.video_codec); else fputs("null", stdout);
    fputs(",\"audio_codec\":", stdout);
    if (result.audio_codec[0]) printf("\"%s\"", result.audio_codec); else fputs("null", stdout);
    if (result.has_video) printf(",\"width\":%d,\"height\":%d", result.width, result.height);
    puts("}");
    return 0;
}
