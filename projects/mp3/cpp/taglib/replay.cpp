#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){if(argc!=2)return 2;FILE*f=fopen(argv[1],"rb");if(!f)return 3;static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}fclose(f);struct parsarium_mp3_result r;if(!parsarium_parse_mp3(data,n,&r))return 5;printf("{\"version\":%u,\"layer\":%u,\"sample_rate\":%u,\"channels\":%u,\"bitrate_kbps\":%u,\"length_ms\":%u}\n",r.version,r.layer,r.sample_rate,r.channels,r.bitrate_kbps,r.length_ms);return 0;}
