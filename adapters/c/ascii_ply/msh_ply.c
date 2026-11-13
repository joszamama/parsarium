#define MSH_PLY_INCLUDE_LIBC_HEADERS
#define MSH_PLY_DECODER_ONLY
#define MSH_PLY_IMPLEMENTATION
#include "msh_ply.h"

int main(int argc, char **argv) {
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

    if (argc != 2) return 2;
    msh_ply_t *file = msh_ply_open(argv[1], "rb");
    if (!file) return 3;
    if (msh_ply_add_descriptor(file, &descriptors[0]) ||
        msh_ply_add_descriptor(file, &descriptors[1]) ||
        msh_ply_read(file) || vertex_count != 3 || face_count != 1) {
        msh_ply_close(file);
        free(vertices);
        free(faces);
        return 4;
    }
    printf("{\"vertices\":%d,\"faces\":%d,\"second_x\":%.1f,\"last_index\":%d}\n",
           vertex_count, face_count, vertices[3], faces[2]);
    free(vertices);
    free(faces);
    msh_ply_close(file);
    return 0;
}
