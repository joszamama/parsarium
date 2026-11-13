#include <ak/assetkit.h>
#include <ak/geom.h>

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_index(const AkAccessor *accessor, unsigned slot, uint32_t *value) {
    const unsigned char *bytes;
    size_t offset;
    size_t width;
    size_t stride;
    if (!accessor || !accessor->buffer || !accessor->buffer->data ||
        slot >= accessor->count) return 0;
    width = accessor->bytesPerComponent;
    stride = accessor->byteStride ? accessor->byteStride : width;
    offset = accessor->byteOffset + (size_t)slot * stride;
    if (offset > accessor->buffer->length || width > accessor->buffer->length - offset) return 0;
    bytes = (const unsigned char *)accessor->buffer->data + offset;
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

int main(int argc, char **argv) {
    AkDoc *doc = NULL;
    AkGeometry *geometry;
    AkMesh *mesh = NULL;
    AkMeshPrimitive *primitive;
    AkAccessor *indices;
    uint32_t face[3];
    unsigned mesh_count = 0;
    unsigned vertex_count;
    unsigned face_count;

    if (argc != 2 || ak_load(&doc, argv[1], AK_FILE_TYPE_AUTO) != AK_OK || !doc) return 1;
    for (geometry = doc->lib.geometries.first; geometry; geometry = geometry->next) {
        AkMesh *candidate = ak_meshFromGeometry(geometry);
        if (candidate) { mesh = candidate; mesh_count++; }
    }
    if (!mesh || !mesh->primitive || mesh_count != 1) { ak_free(doc); return 2; }
    primitive = mesh->primitive;
    indices = ak_meshPrimitiveIndexAccessor(primitive);
    if (!primitive->pos || !primitive->pos->accessor ||
        primitive->type != AK_PRIMITIVE_TRIANGLES || primitive->nPolygons != 1 ||
        ak_meshPrimitiveIndexCount(primitive) != 3 ||
        !read_index(indices, 0, &face[0]) ||
        !read_index(indices, 1, &face[1]) ||
        !read_index(indices, 2, &face[2])) { ak_free(doc); return 3; }
    vertex_count = primitive->pos->accessor->count;
    face_count = primitive->nPolygons;
    printf("{\"meshes\":%u,\"vertices\":%u,\"faces\":%u,\"face\":[%u,%u,%u]}\n",
           mesh_count, vertex_count, face_count, face[0], face[1], face[2]);
    ak_free(doc);
    return 0;
}
