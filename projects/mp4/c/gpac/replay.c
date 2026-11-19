#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp4_result result;
 if(!parsarium_parse_mp4(data,n,&result))return 5;
 printf("{\"tracks\":%u,\"video_tracks\":%u,\"audio_tracks\":%u",result.tracks,result.video_tracks,result.audio_tracks);
 if(result.has_size)printf(",\"width\":%u,\"height\":%u",result.width,result.height);
 if(result.has_duration)printf(",\"duration_ms\":%llu",result.duration_ms);
 printf("}\n");
 return 0;
}
