#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
static int first = 1;
static void field(const char *name, const char *value, int number) {
    if (!value) return;
    printf("%s\"%s\":", first ? "" : ",", name);
    first = 0;
    if (number) { printf("%ld", strtol(value, NULL, 10)); return; }
    putchar('"');
    for (const unsigned char *p = (const unsigned char *)value; *p; ++p) {
        if (*p == '"' || *p == '\\') printf("\\%c", *p);
        else if (*p < 32) printf("\\u%04x", *p);
        else putchar(*p);
    }
    putchar('"');
}
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb"); if (!file) return 3;
    static uint8_t data[1u << 20]; size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) { fclose(file); return 4; }
    fclose(file);
    struct parsarium_mp4_result result;
    if (!parsarium_parse_mp4(data, size, &result)) return 5;
    putchar('{');
    field("container", result.container, 0);
    field("title", result.title, 0);
    field("video", result.video, 0);
    field("audio", result.audio, 0);
    field("width", result.width, 1);
    field("height", result.height, 1);
    puts("}");
    parsarium_free_mp4(&result);
    return 0;
}
