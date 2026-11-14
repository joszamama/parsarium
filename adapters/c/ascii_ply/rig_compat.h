/* Observation-only stand-ins for Rig's GPU and mesh allocation layer.
 * The tagged rut-mesh-ply.c and rply.c parser sources are compiled unchanged.
 */
#ifndef PARSARIUM_RIG_COMPAT_H
#define PARSARIUM_RIG_COMPAT_H

#include <glib.h>
#include <stdint.h>
#include <stddef.h>

#define _RUT_MESH_H_
#define _RUT_INTERFACES_H_

typedef int CoglBool;
typedef void CoglContext;
typedef enum { COGL_VERTICES_MODE_TRIANGLES = 3 } CoglVerticesMode;
typedef enum {
  COGL_INDICES_TYPE_UNSIGNED_BYTE,
  COGL_INDICES_TYPE_UNSIGNED_SHORT,
  COGL_INDICES_TYPE_UNSIGNED_INT
} CoglIndicesType;
#define COGL_FEATURE_ID_UNSIGNED_INT_INDICES 1
static inline CoglBool cogl_has_feature(CoglContext *ctx, int feature)
{ (void)ctx; (void)feature; return TRUE; }

typedef enum {
  RUT_ATTRIBUTE_TYPE_BYTE,
  RUT_ATTRIBUTE_TYPE_UNSIGNED_BYTE,
  RUT_ATTRIBUTE_TYPE_SHORT,
  RUT_ATTRIBUTE_TYPE_UNSIGNED_SHORT,
  RUT_ATTRIBUTE_TYPE_FLOAT
} RutAttributeType;

typedef struct { CoglContext *cogl_context; } RutContext;
typedef struct _RutBuffer { uint8_t *data; size_t size; } RutBuffer;
typedef struct _RutAttribute {
  RutBuffer *buffer;
  const char *name;
  size_t stride, offset;
  int n_components;
  RutAttributeType type;
} RutAttribute;
typedef struct _RutMesh {
  CoglVerticesMode mode;
  int n_vertices, n_attributes, n_indices;
  RutAttribute **attributes;
  CoglIndicesType indices_type;
  RutBuffer *indices_buffer;
} RutMesh;

RutBuffer *rut_buffer_new(size_t size);
RutAttribute *rut_attribute_new(RutBuffer *buffer, const char *name,
                                size_t stride, size_t offset,
                                int n_components, RutAttributeType type);
RutMesh *rut_mesh_new(CoglVerticesMode mode, int n_vertices,
                      RutAttribute **attributes, int n_attributes);
void rut_mesh_set_indices(RutMesh *mesh, CoglIndicesType type,
                          RutBuffer *buffer, int n_indices);
void rut_refable_unref(void *object);

#endif
