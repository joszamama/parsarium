#include "harness.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) {
        fclose(file);
        return 4;
    }
    fclose(file);
    struct parsarium_wav_result result = {0};
    if (!parsarium_parse_wav(data, size, &result)) {
        if (result.error[0]) fprintf(stderr, "%s\n", result.error);
        return 5;
    }
    printf("{\"sample_rate\":%u,\"channels\":%u,\"frames\":%llu,\"samples\":[",
           result.sample_rate, result.channels, result.frames);
    for (unsigned i = 0; i < result.sample_count && i < 4; i++)
        printf("%s%d", i ? "," : "", result.samples[i]);
    printf("]}\n");
    return 0;
}
