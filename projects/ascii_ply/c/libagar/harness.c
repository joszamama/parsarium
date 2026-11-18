#define _GNU_SOURCE
#define _USE_AGAR_TYPES
#include "harness.h"

#include <agar/core.h>
#include <agar/gui.h>
#include <agar/sg.h>
#include <agar/sg/sg_load_ply.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* AG_ObjectDestroy() of an SG_Object calls SG_ObjectFreeGeometry(), which reallocates empty
 * vertex/edge/facet tables during teardown and does not release them (upstream sg_object.c).
 * That teardown allocation is not parser behaviour; leak reports are off, as for atril. */
const char *__asan_default_options(void) { return "detect_leaks=0"; }

static int initialized;

static int initialize(void) {
    if (initialized) return initialized > 0;
    /* Agar-Core and Agar-SG only: no GUI driver is opened (agGUI stays unset). */
    if (AG_InitCore(NULL, 0) == -1) {
        initialized = -1;
        return 0;
    }
    SG_InitSubsystem();
    initialized = 1;
    return 1;
}

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    if (!initialize()) return 0;
    char directory[] = "/tmp/parsarium-libagar-XXXXXX";
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
    /* Documented SG_Object(3) API: SG_ObjectNew() then SG_ObjectLoadPLY(local path). */
    SG_Object *so = SG_ObjectNew(NULL, "parsarium");
    if (written && SG_ObjectLoadPLY(so, path, 0) == 0) {
        /* SG_Object vertex index 0 is reserved; loaded vertices start at 1. */
        result->vertices = so->nVtx > 0 ? so->nVtx - 1 : 0;
        result->faces = 0;
        SG_Facet *first = NULL;
        for (Uint bucket = 0; bucket < so->nFacetTbl; bucket++) {
            SG_Facet *facet;
            AG_SLIST_FOREACH(facet, &so->facetTbl[bucket].facets, facets) {
                result->faces++;
                if (!first) first = facet;
            }
        }
        for (int i = 0; i < 3; ++i) result->face[i] = 0;
        if (first && first->n >= 3) {
            for (int i = 0; i < 3; ++i) {
                /* Halfedge e[k] runs v[k] -> v[k+1] and stores its destination vertex. */
                SG_Edge *edge = first->e[(i + 2) % 3];
                int vertex = edge ? edge->v : 0;
                result->face[i] = vertex > 0 ? (unsigned)(vertex - 1) : 0;
            }
        }
        okay = 1;
    }
    AG_ObjectDestroy(so);
    unlink(path);
    rmdir(directory);
    return okay;
}
