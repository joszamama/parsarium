#include "rply.h"
#include <cstdio>

struct Result {
  long vertices_seen = 0;
  long face_values_seen = 0;
  long face[3] = {};
};

static int vertex_cb(p_ply_argument argument) {
  void *data = nullptr;
  if (!ply_get_argument_user_data(argument, &data, nullptr)) return 0;
  ++static_cast<Result *>(data)->vertices_seen;
  return 1;
}

static int face_cb(p_ply_argument argument) {
  void *data = nullptr;
  long length = 0, index = -1;
  if (!ply_get_argument_user_data(argument, &data, nullptr) ||
      !ply_get_argument_property(argument, nullptr, &length, &index)) return 0;
  if (length != 3) return 0;
  if (index >= 0 && index < 3) {
    auto *out = static_cast<Result *>(data);
    out->face[index] = static_cast<long>(ply_get_argument_value(argument));
    ++out->face_values_seen;
  }
  return 1;
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  Result out;
  p_ply ply = ply_open(argv[1], nullptr, 0, nullptr);
  if (!ply || !ply_read_header(ply)) return 1;
  long vertices = ply_set_read_cb(ply, "vertex", "x", vertex_cb, &out, 0);
  long faces = ply_set_read_cb(ply, "face", "vertex_indices", face_cb, &out, 0);
  if (vertices != 3 || faces != 1 || !ply_read(ply) ||
      out.vertices_seen != 3 || out.face_values_seen != 3) return 1;
  std::printf("{\"vertices\":%ld,\"faces\":%ld,\"face\":[%ld,%ld,%ld]}\n",
              vertices, faces, out.face[0], out.face[1], out.face[2]);
  ply_close(ply);
  return 0;
}
