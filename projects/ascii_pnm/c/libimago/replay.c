#include "harness.h"
#include <stdio.h>
int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "rb"); if (!file) return 3;
  uint8_t data[1u << 20]; size_t size = fread(data, 1, sizeof(data), file);
  if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) { fclose(file); return 4; }
  fclose(file);
  struct parsarium_pnm_result r;
  if (!parsarium_parse_pnm(data, size, &r)) return 5;
  printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
         r.width, r.height, r.first[0], r.first[1], r.first[2], r.first[3],
         r.second[0], r.second[1], r.second[2], r.second[3]);
  return 0;
}
