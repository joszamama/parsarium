#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){if(argc!=2)return 2;FILE*f=fopen(argv[1],"rb");if(!f)return 3;uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}fclose(f);struct parsarium_id3_result r;if(!parsarium_parse_id3(data,n,&r))return 5;printf("{\"title\":\"%s\",\"normalized_id3_major\":%u,\"frames\":%u}\n",r.title,r.normalized_id3_major,r.frames);return 0;}
