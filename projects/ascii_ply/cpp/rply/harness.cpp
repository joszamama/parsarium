#include "harness.h"
#include <rply.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

struct read_state { long vertices_seen; long face_values_seen; long face[3]; };
static int vertex_cb(p_ply_argument argument) {
    void *data = NULL;
    if (!ply_get_argument_user_data(argument, &data, NULL)) return 0;
    struct read_state *state = (struct read_state *)data;
    ++state->vertices_seen;
    return 1;
}
static int face_cb(p_ply_argument argument) {
    void *data = NULL; long length = 0, index = -1;
    if (!ply_get_argument_user_data(argument, &data, NULL) ||
        !ply_get_argument_property(argument, NULL, &length, &index)) return 0;
    struct read_state *state = (struct read_state *)data;
    if (length != 3) return 0;
    if (index >= 0 && index < 3) {
        state->face[index] = (long)ply_get_argument_value(argument);
        ++state->face_values_seen;
    }
    return 1;
}
int parsarium_parse_ply(const uint8_t *data, size_t size, struct parsarium_ply_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    char path[] = "/tmp/parsarium-ply-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t written = write(fd, data + offset, size - offset);
        if (written <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)written;
    }
    close(fd);
    p_ply ply = ply_open(path, NULL, 0, NULL);
    unlink(path);
    if (!ply) return 0;
    struct read_state state = {0};
    int ok = 0;
    if (ply_read_header(ply)) {
        long vertices = ply_set_read_cb(ply, "vertex", "x", vertex_cb, &state, 0);
        long faces = ply_set_read_cb(ply, "face", "vertex_indices", face_cb, &state, 0);
        if (vertices > 0 && faces > 0 && vertices <= 100000 && faces <= 100000 &&
            ply_read(ply) && state.vertices_seen == vertices &&
            state.face_values_seen == 3) {
            result->vertices = vertices; result->faces = faces;
            for (int i = 0; i < 3; i++) result->face[i] = state.face[i];
            ok = 1;
        }
    }
    ply_close(ply);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ply_result result;
    (void)parsarium_parse_ply(data, size, &result);
    return 0;
}
