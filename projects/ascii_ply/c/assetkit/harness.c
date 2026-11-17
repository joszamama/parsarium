#define _GNU_SOURCE
#include "harness.h"

#include <ak/assetkit.h>
#include <ak/geom.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static int read_index(const AkAccessor *accessor, unsigned slot, uint32_t *value) {
    if (!accessor || !accessor->buffer || !accessor->buffer->data ||
        slot >= accessor->count) return 0;
    size_t width = accessor->bytesPerComponent;
    size_t stride = accessor->byteStride ? accessor->byteStride : width;
    size_t offset = accessor->byteOffset + (size_t)slot * stride;
    if (offset > accessor->buffer->length || width > accessor->buffer->length - offset)
        return 0;
    const unsigned char *bytes = (const unsigned char *)accessor->buffer->data + offset;
    switch (accessor->componentType) {
        case AKT_UBYTE: *value = bytes[0]; return 1;
        case AKT_USHORT: {
            uint16_t item;
            memcpy(&item, bytes, sizeof(item));
            *value = item;
            return 1;
        }
        case AKT_UINT: memcpy(value, bytes, sizeof(*value)); return 1;
        default: return 0;
    }
}

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    char directory[] = "/tmp/parsarium-assetkit-XXXXXX";
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

    AkDoc *doc = NULL;
    int okay = 0;
    if (written && ak_load(&doc, path, AK_FILE_TYPE_AUTO) == AK_OK && doc) {
        AkMesh *mesh = NULL;
        unsigned mesh_count = 0;
        for (AkGeometry *geometry = doc->lib.geometries.first; geometry;
             geometry = geometry->next) {
            AkMesh *candidate = ak_meshFromGeometry(geometry);
            if (candidate) { mesh = candidate; mesh_count++; }
        }
        if (mesh && mesh->primitive) {
            AkMeshPrimitive *primitive = mesh->primitive;
            AkAccessor *indices = ak_meshPrimitiveIndexAccessor(primitive);
            if (primitive->pos && primitive->pos->accessor) {
                result->meshes = mesh_count;
                result->vertices = primitive->pos->accessor->count;
                result->faces = (primitive->type == AK_PRIMITIVE_TRIANGLES ||
                                 primitive->type == AK_PRIMITIVE_POLYGONS)
                                    ? primitive->nPolygons : 0;
                for (int i = 0; i < 3; ++i) result->face[i] = 0;
                if (result->faces && indices &&
                    ak_meshPrimitiveIndexCount(primitive) >= 3) {
                    for (int i = 0; i < 3; ++i) {
                        if (!read_index(indices, (unsigned)i, &result->face[i]))
                            result->face[i] = 0;
                    }
                }
                okay = 1;
            }
        }
    }
    if (doc) ak_free(doc);
    unlink(path);
    rmdir(directory);
    return okay;
}
