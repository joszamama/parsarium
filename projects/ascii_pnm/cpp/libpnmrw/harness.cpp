#define _GNU_SOURCE
#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern "C" {
#include "libpnmrw.h"
}
int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
 if (!data || !result || !size || size > (1u << 20)) return 0;
 memset(result,0,sizeof(*result));
 unsigned char *copy = (unsigned char *)malloc(size);
 if (!copy) return 0;
 memcpy(copy,data,size);
 FILE *file = fmemopen(copy,size,"rb");
 if (!file) { free(copy); return 0; }
 pnm_init2((char *)"parsarium");
 int width=0,height=0,format=0;
 xelval maxval=0;
 xel **pixels=pnm_readpnm(file,&width,&height,&maxval,&format);
 fclose(file);
 free(copy);
 if (!pixels || width < 2 || height < 1 || format != PPM_FORMAT) {
  if (pixels) pnm_freearray(pixels,height);
  return 0;
 }
 result->width=width; result->height=height; result->maxval=maxval;
 result->first[0]=PPM_GETR(pixels[0][0]);
 result->first[1]=PPM_GETG(pixels[0][0]);
 result->first[2]=PPM_GETB(pixels[0][0]);
 result->second[0]=PPM_GETR(pixels[0][1]);
 result->second[1]=PPM_GETG(pixels[0][1]);
 result->second[2]=PPM_GETB(pixels[0][1]);
 pnm_freearray(pixels,height);
 return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
 struct parsarium_pnm_result result;
 (void)parsarium_parse_pnm(data,size,&result);
 return 0;
}
