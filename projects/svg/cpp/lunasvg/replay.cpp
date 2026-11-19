#include "harness.h"
#include <stdio.h>
int main(int argc,char**argv){if(argc!=2)return 2;FILE*f=fopen(argv[1],"rb");if(!f)return 3;uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}fclose(f);struct parsarium_svg_result r;if(!parsarium_parse_svg(data,n,&r))return 5;printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u],\"second\":",r.width,r.height,r.first[0],r.first[1],r.first[2]);if(r.second_present)printf("[%u,%u,%u]",r.second[0],r.second[1],r.second[2]);else fputs("null",stdout);puts("}");return 0;}
