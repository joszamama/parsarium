#include "harness.h"
#include <stdio.h>

static void json_string(const char *text) {
    putchar('"');
    for (const unsigned char *p = (const unsigned char *)text; *p; ++p) {
        if (*p == '"' || *p == '\\') { putchar('\\'); putchar(*p); }
        else if (*p < 32) printf("\\u%04x", *p);
        else putchar(*p);
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    static uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) { fclose(file); return 4; }
    fclose(file);
    struct parsarium_result result;
    if (!parsarium_parse(data, size, &result)) return 5;
    printf("{\"title\":");
    json_string(result.title);
    printf(",\"audio_tracks\":%u,\"mp3_tracks\":%u,\"audio_codec\":",
           result.audio_tracks, result.mp3_tracks);
    json_string(result.audio_codec);
    printf(",\"rate\":%u,\"channels\":%u}\n", result.rate, result.channels);
    return 0;
}
