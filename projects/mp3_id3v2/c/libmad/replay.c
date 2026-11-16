#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){if(argc!=2)return 2;FILE*f=fopen(argv[1],"rb");if(!f)return 3;uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}fclose(f);struct parsarium_mp3_result r;if(!parsarium_parse_mp3(data,n,&r))return 5;printf("{\"layer\":%u,\"sample_rate\":%u,\"bit_rate\":%lu,\"channels\":%u,\"decoded_samples\":%u}\n",r.layer,r.sample_rate,r.bit_rate,r.channels,r.decoded_samples);return 0;}
