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
    printf("{\"split_status\":%d,\"segment_bytes\":%zu,\"frame_header\":\"%02x%02x%02x%02x\"}\n", result.split_status, result.segment_bytes, result.first[0], result.first[1], result.first[2], result.first[3]);
    return 0;
}
