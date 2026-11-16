#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv) {
 if(argc!=2)return 2;FILE *file=fopen(argv[1],"rb");if(!file)return 3;
 uint8_t data[1u<<20];size_t size=fread(data,1,sizeof(data),file);
 if(ferror(file)||(size==sizeof(data)&&fgetc(file)!=EOF)){fclose(file);return 4;}
 fclose(file);struct parsarium_mp3_result r;if(!parsarium_parse_mp3(data,size,&r))return 5;
 printf("{\"sample_rate\":%u,\"channels\":%u,\"decoded_frames\":%llu,\"id3v2_bytes\":%zu}\n",r.sample_rate,r.channels,(unsigned long long)r.decoded_frames,r.id3v2_bytes);
 return 0;
}
