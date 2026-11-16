#include "harness.h"
#include <stdio.h>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) { fclose(file); return 4; }
    fclose(file);
    Result result;
    if (!parse_data(data, size, &result)) return 5;
    printf("{\"samples\":%llu,\"sample_rate\":%u,\"channels\":%u}\n", (unsigned long long)result.samples, result.sample_rate, result.channels);
    return 0;
}
