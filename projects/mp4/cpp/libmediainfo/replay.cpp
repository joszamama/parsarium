#include "harness.h"
#include <stdio.h>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb"); if (!file) return 3;
    uint8_t data[1u << 20]; size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) { fclose(file); return 4; }
    fclose(file);
    struct parsarium_mp4_result result;
    if (!parsarium_parse_mp4(data, size, &result)) return 5;
    printf("{\"container\":\"%s\",\"title\":\"%s\",\"video\":\"%s\",\"audio\":\"%s\",\"width\":%d,\"height\":%d}\n",
           result.container, result.title, result.video, result.audio, result.width, result.height);
    return 0;
}
