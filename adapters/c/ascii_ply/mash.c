#include "mash_compat.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* Cogl upload functions retain parsed fields for the control's output. */
typedef struct {
  int n;
  float second_x;
} VertexCapture;
typedef struct {
  int n;
  unsigned int face[3];
} IndexCapture;
static VertexCapture *vertices;
static IndexCapture *indices;
CoglHandle cogl_vertex_buffer_new(guint n) {
  vertices = calloc(1, sizeof(*vertices));
  vertices->n = n;
  return vertices;
}
void cogl_vertex_buffer_add(CoglHandle h, const char *name, int comps, int type,
                            gboolean norm, guint stride, const void *data) {
  (void)comps;
  (void)type;
  (void)norm;
  if (!strcmp(name, "gl_Vertex")) {
    VertexCapture *v = h;
    memcpy(&v->second_x, (const unsigned char *)data + stride, 4);
  }
}
void cogl_vertex_buffer_submit(CoglHandle h) { (void)h; }
CoglHandle cogl_vertex_buffer_indices_new(CoglIndicesType type,
                                          const void *data, guint count) {
  indices = calloc(1, sizeof(*indices));
  indices->n = count;
  for (int n = 0; n < 3; n++) {
    if (type == COGL_INDICES_TYPE_UNSIGNED_BYTE)
      indices->face[n] = ((const guint8 *)data)[n];
    else if (type == COGL_INDICES_TYPE_UNSIGNED_SHORT)
      indices->face[n] = ((const guint16 *)data)[n];
    else
      indices->face[n] = ((const guint32 *)data)[n];
  }
  return indices;
}
void cogl_vertex_buffer_draw_elements(CoglHandle a, int mode, CoglHandle b,
                                      guint c, guint d, guint e, guint f) {
  (void)a;
  (void)mode;
  (void)b;
  (void)c;
  (void)d;
  (void)e;
  (void)f;
}
CoglHandle cogl_handle_ref(CoglHandle h) { return h; }
void cogl_handle_unref(CoglHandle h) { (void)h; }
gboolean cogl_features_available(int feature) {
  (void)feature;
  return TRUE;
}
int main(int argc, char **argv) {
  if (argc != 2)
    return 2;
  MashData *data = mash_data_new();
  GError *error = NULL;
  if (!mash_data_load(data, MASH_DATA_NONE, argv[1], &error)) {
    fprintf(stderr, "%s\n", error ? error->message : "unknown");
    return 1;
  }
  if (!vertices || !indices || indices->n < 3)
    return 3;
  ClutterVertex min, max;
  mash_data_get_extents(data, &min, &max);
  printf("{\"vertices\":%d,\"indices\":%d,\"face\":[%u,%u,%u],"
         "\"second_x\":%.1f,\"min_x\":%.1f,\"max_x\":%.1f}\n",
         vertices->n, indices->n, indices->face[0], indices->face[1],
         indices->face[2], vertices->second_x, min.x, max.x);
  return 0;
}
