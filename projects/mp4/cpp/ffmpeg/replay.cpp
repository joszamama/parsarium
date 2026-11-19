#include "harness.h"
#include <stdio.h>
static void json_string(const char *s){
 putchar('"');
 for(;*s;++s){unsigned char c=(unsigned char)*s;
  if(c=='"'||c=='\\')printf("\\%c",c);else if(c<0x20)printf("\\u%04x",c);else putchar(c);}
 putchar('"');
}
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp4_result result;
 if(!parsarium_parse_mp4(data,n,&result))return 5;
 /* Metadata entries the demuxer did not report, and the size of an absent
    video stream, are omitted. */
 putchar('{');
 if(result.brand){printf("\"brand\":");json_string(result.brand);putchar(',');}
 if(result.title){printf("\"title\":");json_string(result.title);putchar(',');}
 printf("\"video_tracks\":%u,\"audio_tracks\":%u",result.video_tracks,result.audio_tracks);
 if(result.video_tracks)printf(",\"width\":%u,\"height\":%u",result.width,result.height);
 printf("}\n");
 parsarium_free_mp4(&result);
 return 0;
}
