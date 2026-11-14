/* Observe PCC's public C point-cloud reader on a local ASCII PLY file. */
#include <pcc/point_cloud.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  pcc_point_cloud_t cloud;
  pcc_point_cloud_init(&cloud);
  cloud.read_from_file(&cloud, argv[1]);
  if (!cloud.positions || cloud.size != 3) {
    pcc_point_cloud_destroy(&cloud);
    return 3;
  }
  printf("{\"vertices\":%u,\"second_x\":%.1f}\n", cloud.size,
         cloud.positions[3]);
  pcc_point_cloud_destroy(&cloud);
  return 0;
}
