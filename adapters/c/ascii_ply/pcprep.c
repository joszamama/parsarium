/* Observe pcprep's public C point-cloud loader on a local ASCII PLY file. */
#include <pcprep/pointcloud.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  pointcloud_t cloud = {0};
  int loaded = pointcloud_load(&cloud, argv[1]);
  if (!loaded || cloud.size != 3 || !cloud.pos) {
    pointcloud_free(&cloud);
    return 3;
  }
  printf("{\"vertices\":%zu,\"second_x\":%.1f}\n", cloud.size,
         cloud.pos[3]);
  pointcloud_free(&cloud);
  return 0;
}
