#define _GNU_SOURCE
#include "harness.h"
#include "stereokit_c_compat.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/* stdlib.h defines key_t, which conflicts with StereoKit 0.3.11's key_t enum. */
extern int mkstemps(char *template, int suffixlen);

int parsarium_parse_ply(const uint8_t *data, size_t size, struct parsarium_ply_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-stereokit-XXXXXX.ply";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    if (close(fd)) { unlink(path); return 0; }

    sk_settings_t settings = {0};
    settings.app_name = "Parsarium PLY control";
    settings.mode = app_mode_offscreen;
    settings.assets_folder = "";
    settings.log_filter = log_warning;
    /* StereoKit writes startup diagnostics to stdout. Keep replay JSON on stdout. */
    fflush(stdout);
    int saved_stdout = dup(STDOUT_FILENO);
    if (saved_stdout < 0 || dup2(STDERR_FILENO, STDOUT_FILENO) < 0) {
        if (saved_stdout >= 0) close(saved_stdout);
        unlink(path);
        return 0;
    }
    if (!sk_init(settings)) {
        fflush(stdout); dup2(saved_stdout, STDOUT_FILENO); close(saved_stdout);
        unlink(path);
        return 0;
    }
    model_t model = model_create_file(path, NULL);
    unlink(path);
    int ok = model && model_subset_count(model) > 0;
    mesh_t mesh = ok ? model_get_mesh(model, 0) : NULL;
    ok = ok && mesh;
    if (ok) {
        vert_t *verts = NULL;
        vind_t *inds = NULL;
        int32_t vertex_count = 0, index_count = 0;
        mesh_get_verts(mesh, &verts, &vertex_count, memory_reference);
        mesh_get_inds(mesh, &inds, &index_count, memory_reference);
        ok = verts && inds && vertex_count > 0 && index_count >= 3;
        if (ok) {
            result->subsets = model_subset_count(model);
            result->vertices = vertex_count;
            result->indices = index_count;
            memcpy(result->face, inds, 3 * sizeof(vind_t));
            result->second_present = vertex_count > 1;
            if (result->second_present) result->second_x = verts[1].pos.x;
        }
    }
    if (mesh) mesh_release(mesh);
    if (model) model_release(model);
    sk_shutdown();
    fflush(stdout);
    dup2(saved_stdout, STDOUT_FILENO);
    close(saved_stdout);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ply_result result;
    (void)parsarium_parse_ply(data, size, &result);
    return 0;
}
