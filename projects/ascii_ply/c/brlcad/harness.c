#define _GNU_SOURCE
#include "harness.h"

#include <unistd.h>

#include "common.h"
#include "gcv/api.h"
#ifdef __APPLE__
#define setmode brlcad_setmode
#endif
#include "raytrace.h"
#ifdef __APPLE__
#undef setmode
#endif

#include <fcntl.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    char directory[] = "/tmp/parsarium-brlcad-XXXXXX";
    if (!mkdtemp(directory)) return 0;
    char path[sizeof(directory) + sizeof("/input.ply")];
    snprintf(path, sizeof(path), "%s/input.ply", directory);
    int fd = open(path, O_CREAT | O_EXCL | O_WRONLY, 0600);
    if (fd < 0) { rmdir(directory); return 0; }
    int written = 1;
    for (size_t offset = 0; offset < size;) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { written = 0; break; }
        offset += (size_t)count;
    }
    if (close(fd) != 0) written = 0;

    int okay = 0;
    if (written) {
        struct gcv_context context;
        gcv_context_init(&context);
        const struct gcv_filter *reader =
            find_filter(GCV_FILTER_READ, BU_MIME_MODEL_PLY, path, &context);
        if (reader) {
            struct gcv_opts options;
            gcv_opts_default(&options);
            options.scale_factor = 1.0;
            if (gcv_execute(&context, reader, &options, 0, NULL, path)) {
                struct directory *entry = db_lookup(context.dbip, "input.bot", LOOKUP_QUIET);
                if (entry) {
                    struct rt_db_internal internal;
                    RT_DB_INTERNAL_INIT(&internal);
                    if (rt_db_get_internal(&internal, entry, context.dbip, NULL) >= 0) {
                        if (internal.idb_minor_type == ID_BOT) {
                            const struct rt_bot_internal *bot =
                                (const struct rt_bot_internal *)internal.idb_ptr;
                            if (bot && bot->num_faces > 0 && bot->num_vertices > 1 &&
                                bot->vertices && bot->faces &&
                                isfinite(bot->vertices[3])) {
                                result->vertices = bot->num_vertices;
                                result->faces = bot->num_faces;
                                result->second_x = bot->vertices[3];
                                for (int i = 0; i < 3; ++i)
                                    result->face[i] = bot->faces[i];
                                okay = 1;
                            }
                        }
                        rt_db_free_internal(&internal);
                    }
                }
            }
        }
        gcv_context_destroy(&context);
    }
    unlink(path);
    rmdir(directory);
    return okay;
}
