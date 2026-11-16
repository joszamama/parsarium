#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}fclose(f);
 struct parsarium_svg_result r;if(!parsarium_parse_svg(data,n,&r))return 5;
 printf("{\"width\":%d,\"height\":%d,\"shapes\":%d,\"paths\":%d}\n",r.width,r.height,r.shapes,r.paths);return 0;}
