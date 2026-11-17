#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp4_result result;
 if(!parsarium_parse_mp4(data,n,&result))return 5;
 printf("{\"brand\":\"%s\",\"tracks\":%u,\"video_tracks\":%u,\"audio_tracks\":%u,\"duration_ms\":%u}\n",
        result.brand,result.tracks,result.video_tracks,result.audio_tracks,result.duration_ms);
 return 0;
}
