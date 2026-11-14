#ifndef COGL_MOCK_H
#define COGL_MOCK_H
#include <glib.h>
typedef void *CoglHandle;
typedef enum {
  COGL_INDICES_TYPE_UNSIGNED_BYTE,
  COGL_INDICES_TYPE_UNSIGNED_SHORT,
  COGL_INDICES_TYPE_UNSIGNED_INT
} CoglIndicesType;
#define COGL_FEATURE_UNSIGNED_INT_INDICES 1
#define COGL_ATTRIBUTE_TYPE_FLOAT 1
#define COGL_ATTRIBUTE_TYPE_UNSIGNED_BYTE 2
#define COGL_VERTICES_MODE_TRIANGLES 3
CoglHandle cogl_vertex_buffer_new(guint n);
void cogl_vertex_buffer_add(CoglHandle h, const char *name, int comps, int type,
                            gboolean norm, guint stride, const void *data);
void cogl_vertex_buffer_submit(CoglHandle h);
CoglHandle cogl_vertex_buffer_indices_new(CoglIndicesType type,
                                          const void *data, guint count);
void cogl_vertex_buffer_draw_elements(CoglHandle a, int mode, CoglHandle b,
                                      guint c, guint d, guint e, guint f);
CoglHandle cogl_handle_ref(CoglHandle h);
void cogl_handle_unref(CoglHandle h);
gboolean cogl_features_available(int feature);
#endif
