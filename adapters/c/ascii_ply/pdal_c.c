#include "pdal/pdalc.h"

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2 || strchr(argv[1], '"') || strchr(argv[1], '\\')) return 2;
  const char *prefix = "{\"pipeline\":[{\"type\":\"readers.ply\",\"filename\":\"";
  const char *suffix = "\"}]}";
  size_t length = strlen(prefix) + strlen(argv[1]) + strlen(suffix) + 1;
  char *json = malloc(length);
  if (!json) return 1;
  snprintf(json, length, "%s%s%s", prefix, argv[1], suffix);
  PDALPipelinePtr pipeline = PDALCreatePipeline(json);
  free(json);
  if (!pipeline) return 1;
  int64_t points = PDALExecutePipeline(pipeline);
  if (points < 0) {
    PDALDisposePipeline(pipeline);
    return 1;
  }
  PDALPointViewIteratorPtr views = PDALGetPointViews(pipeline);
  if (!views || !PDALHasNextPointView(views)) {
    PDALDisposePointViewIterator(views);
    PDALDisposePipeline(pipeline);
    return 1;
  }
  PDALPointViewPtr view = PDALGetNextPointView(views);
  uint64_t view_points = PDALGetPointViewSize(view);
  uint64_t triangles = PDALGetMeshSize(view);
  printf("{\"points\":%" PRId64 ",\"view_points\":%" PRIu64 ",\"triangles\":%" PRIu64 "}\n",
         points, view_points, triangles);
  PDALDisposePointView(view);
  PDALDisposePointViewIterator(views);
  PDALDisposePipeline(pipeline);
  return 0;
}
