#include "harness.h"
#define MICRO_PLY_IMPL
#include <micro_ply.h>
#include <stdlib.h>
#include <string.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                       struct parsarium_ply_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    uint8_t *bytes = malloc(size + 1);
    if (!bytes) return 0;
    memcpy(bytes, data, size);
    bytes[size] = 0;
    ply_file_t ply = {0};
    if (!ply_read(bytes, size, &ply)) { free(bytes); return 0; }
    int32_t vertices = -1, faces = -1;
    for (int32_t i = 0; i < ply.count; ++i) {
        if (!strcmp(ply.elements[i].name, PLY_ELEMENT_VERTICES))
            vertices = ply.elements[i].count;
        if (!strcmp(ply.elements[i].name, PLY_ELEMENT_FACES))
            faces = ply.elements[i].count;
    }
    float zero = 0.0f;
    ply_map_t map[] = {
        {PLY_PROP_POSITION_X, ply_prop_decimal, sizeof(float), 0, &zero},
        {PLY_PROP_POSITION_Y, ply_prop_decimal, sizeof(float), 4, &zero},
        {PLY_PROP_POSITION_Z, ply_prop_decimal, sizeof(float), 8, &zero},
    };
    float *positions = NULL;
    int32_t converted = 0;
    ply_convert(&ply, PLY_ELEMENT_VERTICES, map, 3, 3 * sizeof(float),
                (void **)&positions, &converted);
    int ok = positions && converted >= 2 && vertices >= 2 && faces >= 1;
    if (ok) {
        result->vertices = vertices;
        result->faces = faces;
        result->converted = converted;
        result->second_x = positions[3];
    }
    free(positions);
    ply_free(&ply);
    free(bytes);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ply_result result;
    (void)parsarium_parse_ply(data, size, &result);
    return 0;
}
