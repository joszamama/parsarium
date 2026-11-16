#include "harness.h"
#define MSH_PLY_INCLUDE_LIBC_HEADERS
#define MSH_PLY_DECODER_ONLY
#define MSH_PLY_IMPLEMENTATION
#include <msh_ply.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                       struct parsarium_ply_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-msh-ply-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)count;
    }
    close(fd);
    float *vertices = NULL;
    int32_t *faces = NULL;
    int32_t vertex_count = 0, face_count = 0;
    msh_ply_desc_t descriptors[2] = {
        {.element_name = "vertex", .property_names = (const char *[]) {"x", "y", "z"},
         .num_properties = 3, .data_type = MSH_PLY_FLOAT,
         .data = &vertices, .data_count = &vertex_count},
        {.element_name = "face", .property_names = (const char *[]) {"vertex_indices"},
         .num_properties = 1, .data_type = MSH_PLY_INT32,
         .list_type = MSH_PLY_UINT8, .list_size_hint = 3,
         .data = &faces, .data_count = &face_count}
    };
    msh_ply_t *file = msh_ply_open(path, "rb");
    int ok = 0;
    if (file && !msh_ply_add_descriptor(file, &descriptors[0]) &&
        !msh_ply_add_descriptor(file, &descriptors[1]) &&
        !msh_ply_read(file) && vertex_count >= 2 && face_count >= 1 &&
        vertices && faces) {
        result->vertices = vertex_count;
        result->faces = face_count;
        result->second_x = vertices[3];
        result->last_index = faces[2];
        ok = 1;
    }
    free(vertices);
    free(faces);
    if (file) msh_ply_close(file);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ply_result result;
    (void)parsarium_parse_ply(data, size, &result);
    return 0;
}
