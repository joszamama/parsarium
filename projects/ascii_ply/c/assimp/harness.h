#ifndef PARSARIUM_ASSIMP_C_PLY_HARNESS_H
#define PARSARIUM_ASSIMP_C_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    unsigned meshes;
    unsigned vertices;
    unsigned faces;
    /* All indices of the first mesh's first face (malloc'd, face_count
     * entries); NULL with face_count 0 when there is no mesh or no face. */
    unsigned *face;
    unsigned face_count;
};

/* Returns 0 when Assimp rejects the input (parsarium_error() says why). */
int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

void parsarium_free_result(struct parsarium_ply_result *result);

/* aiGetErrorString(): why the last import failed. */
const char *parsarium_error(void);

#endif
