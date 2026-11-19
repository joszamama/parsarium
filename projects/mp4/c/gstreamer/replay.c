#include "harness.h"
#include <stdio.h>

static void json_title(const char *title) {
    putchar('"');
    for (const unsigned char *p = (const unsigned char *)title; *p; ++p) {
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
    uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) { fclose(file); return 4; }
    fclose(file);
    struct parsarium_result result;
    if (!parsarium_parse(data, size, &result)) return 5;
    putchar('{');
    if (result.title) { printf("\"title\":"); json_title(result.title); putchar(','); }
    printf("\"video_tracks\":%u,\"audio_tracks\":%u", result.video_tracks, result.audio_tracks);
    if (result.video_tracks) printf(",\"width\":%u,\"height\":%u", result.width, result.height);
    printf("}\n");
    parsarium_free(&result);

    return 0;
}
