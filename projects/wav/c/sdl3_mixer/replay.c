#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 uint8_t data[1u<<20];size_t size=fread(data,1,sizeof(data),f);
 if(ferror(f)||(size==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}fclose(f);
 struct parsarium_wav_result result;if(!parsarium_parse_wav(data,size,&result))return 5;
 printf("{\"sample_rate\":%u,\"channels\":%u,\"frames\":%llu}\n",result.sample_rate,result.channels,result.frames);
 return 0;
}
