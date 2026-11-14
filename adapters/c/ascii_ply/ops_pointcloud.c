#include "ops_pointcloud.h"

#include <inttypes.h>
#include <stdio.h>
#include <string.h>

struct summary {
  uint64_t count;
  double second_x;
  double last_y;
};

static int32_t collect(const OpsPoint *points, size_t count, void *user_data) {
  struct summary *result = user_data;
  for (size_t i = 0; i < count; ++i) {
    if (result->count == 1) result->second_x = points[i].x;
    if (result->count == 2) result->last_y = points[i].y;
    result->count++;
  }
  return 0;
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  OpsCloud *cloud = NULL;
  OpsStatus status = ops_cloud_open(argv[1], &cloud);
  if (status != OPS_OK) {
    fprintf(stderr, "ops_cloud_open: %s\n", ops_last_error());
    return 1;
  }
  OpsCloudInfo info;
  memset(&info, 0, sizeof info);
  info.struct_size = sizeof info;
  status = ops_cloud_info(cloud, &info);
  struct summary result = {0};
  if (status == OPS_OK) status = ops_cloud_read(cloud, NULL, 8, collect, &result);
  if (status != OPS_OK || info.point_count != result.count) {
    fprintf(stderr, "ops_cloud_read: %s\n", ops_last_error());
    ops_cloud_free(cloud);
    return 1;
  }
  printf("{\"points\":%" PRIu64 ",\"second_x\":%.1f,\"last_y\":%.1f}\n",
         result.count, result.second_x, result.last_y);
  ops_cloud_free(cloud);
  return 0;
}
