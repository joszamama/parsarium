#include "rply.h"
#include <stdio.h>

struct result {
  long vertices_seen;
  long face_values_seen;
  long face[3];
};

static int vertex_cb(p_ply_argument argument) {
  void *data = NULL;
  if (!ply_get_argument_user_data(argument, &data, NULL)) return 0;
  struct result *out = (struct result *)data;
  ++out->vertices_seen;
  return 1;
}

static int face_cb(p_ply_argument argument) {
  void *data = NULL;
  long length = 0, index = -1;
  if (!ply_get_argument_user_data(argument, &data, NULL) ||
      !ply_get_argument_property(argument, NULL, &length, &index)) return 0;
  struct result *out = (struct result *)data;
  if (length != 3) return 0;
  if (index >= 0 && index < 3) {
    out->face[index] = (long)ply_get_argument_value(argument);
    ++out->face_values_seen;
  }
  return 1;
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  struct result out = {0};
  p_ply ply = ply_open(argv[1], NULL, 0, NULL);
  if (!ply) return 1;
  if (!ply_read_header(ply)) return 1;
  long vertices = ply_set_read_cb(ply, "vertex", "x", vertex_cb, &out, 0);
  long faces = ply_set_read_cb(ply, "face", "vertex_indices", face_cb, &out, 0);
  if (vertices != 3 || faces != 1 || !ply_read(ply) ||
      out.vertices_seen != 3 || out.face_values_seen != 3) return 1;
  printf("{\"vertices\":%ld,\"faces\":%ld,\"face\":[%ld,%ld,%ld]}\n",
         vertices, faces, out.face[0], out.face[1], out.face[2]);
  ply_close(ply);
  return 0;
}
