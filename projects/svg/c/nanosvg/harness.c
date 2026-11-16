#include "harness.h"
#include <stdlib.h>
#include <string.h>
#define NANOSVG_IMPLEMENTATION
#include <nanosvg.h>
int parsarium_parse_svg(const uint8_t *data,size_t size,struct parsarium_svg_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 char *text=malloc(size+1);if(!text)return 0;memcpy(text,data,size);text[size]=0;
 NSVGimage *image=nsvgParse(text,"px",96.0f);free(text);if(!image)return 0;
 result->width=(int)image->width;result->height=(int)image->height;
 result->shapes=0;result->paths=0;
 for(NSVGshape *shape=image->shapes;shape;shape=shape->next){
  ++result->shapes;for(NSVGpath *path=shape->paths;path;path=path->next)++result->paths;
 }
 nsvgDelete(image);return result->width>0&&result->height>0;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_svg_result r;(void)parsarium_parse_svg(data,size,&r);return 0;}
