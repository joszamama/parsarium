#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp4_result result;result.error[0]=0;
 if(!parsarium_parse_mp4(data,n,&result)){if(result.error[0])fprintf(stderr,"%s\n",result.error);return 5;}
 printf("{\"sequence_tracks\":%u,\"video_tracks\":%u",result.sequence_tracks,result.video_tracks);
 if(result.video_tracks)printf(",\"width\":%u,\"height\":%u",result.width,result.height);
 printf("}\n");
 return 0;
}
