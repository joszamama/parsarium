#define _GNU_SOURCE
#include "harness.h"
#include <pnmio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int parsarium_parse_pnm(const uint8_t *data,size_t size,struct parsarium_pnm_result *result) {
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 unsigned char *copy=(unsigned char *)malloc(size);if(!copy)return 0;
 memcpy(copy,data,size);FILE *file=fmemopen(copy,size,"rb");
 if(!file){free(copy);return 0;}
 int width=0,height=0,maxval=0,ascii=0;
 (void)read_ppm_header(file,&width,&height,&maxval,&ascii);
 if(width<2||height<1||ascii!=1||maxval<=0){fclose(file);free(copy);return 0;}
 int *pixels=(int *)calloc(size+3,sizeof(int));
 if(!pixels){fclose(file);free(copy);return 0;}
 read_ppm_data(file,pixels,ascii);
 fclose(file);free(copy);
 result->width=width;result->height=height;result->maxval=maxval;
 for(int i=0;i<3;i++){result->first[i]=pixels[i];result->second[i]=pixels[i+3];}
 free(pixels);return 1;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_pnm_result result;(void)parsarium_parse_pnm(data,size,&result);return 0;
}
