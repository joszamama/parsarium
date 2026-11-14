#include "rig_compat.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "rut-mesh-ply.h"

/* Keep the parsed objects alive until main has inspected them. */
RutBuffer *rut_buffer_new(size_t size)
{
  RutBuffer *b = calloc(1, sizeof(*b));
  b->data = calloc(size ? size : 1, 1);
  b->size = size;
  return b;
}

RutAttribute *rut_attribute_new(RutBuffer *buffer, const char *name,
                                size_t stride, size_t offset,
                                int n_components, RutAttributeType type)
{
  RutAttribute *a = calloc(1, sizeof(*a));
  *a = (RutAttribute){buffer, name, stride, offset, n_components, type};
  return a;
}

RutMesh *rut_mesh_new(CoglVerticesMode mode, int n_vertices,
                      RutAttribute **attributes, int n_attributes)
{
  RutMesh *m = calloc(1, sizeof(*m));
  *m = (RutMesh){.mode=mode, .n_vertices=n_vertices,
                 .n_attributes=n_attributes};
  m->attributes = calloc(n_attributes, sizeof(*m->attributes));
  memcpy(m->attributes, attributes, n_attributes * sizeof(*attributes));
  return m;
}

void rut_mesh_set_indices(RutMesh *mesh, CoglIndicesType type,
                          RutBuffer *buffer, int n_indices)
{
  mesh->indices_type = type;
  mesh->indices_buffer = buffer;
  mesh->n_indices = n_indices;
}

void rut_refable_unref(void *object) { (void)object; }

int main(int argc, char **argv)
{
  if (argc != 2) return 2;
  RutContext context = {0};
  RutPLYAttribute position = {
    .name = "position",
    .properties = {{"x", FALSE}, {"y", FALSE}, {"z", FALSE}},
    .n_properties = 3,
    .min_components = 3,
    .required = TRUE
  };
  RutPLYAttributeStatus status;
  GError *error = NULL;
  RutMesh *mesh = rut_mesh_new_from_ply(&context, argv[1], &position,
                                        1, &status, &error);
  if (!mesh || error) {
    fprintf(stderr, "%s\n", error ? error->message : "no mesh");
    return 1;
  }
  if (status != RUT_PLY_ATTRIBUTE_STATUS_LOADED || mesh->n_attributes != 1 ||
      mesh->attributes[0]->type != RUT_ATTRIBUTE_TYPE_FLOAT ||
      mesh->n_indices != 3 || mesh->indices_type != COGL_INDICES_TYPE_UNSIGNED_BYTE)
    return 3;
  RutAttribute *a = mesh->attributes[0];
  float second_x;
  memcpy(&second_x, a->buffer->data + a->stride + a->offset, sizeof(second_x));
  uint8_t *indices = mesh->indices_buffer->data;
  printf("{\"vertices\":%d,\"indices\":%d,\"face\":[%u,%u,%u],\"second_x\":%.1f}\n",
         mesh->n_vertices, mesh->n_indices,
         indices[0], indices[1], indices[2], second_x);
  return 0;
}
