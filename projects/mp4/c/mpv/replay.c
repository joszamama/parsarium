#include "harness.h"
#include <stdio.h>

/* Replay only records coverage and output. libass and fontconfig keep
   process-lifetime allocations, so leak reports at exit are not parser
   results here; the fuzzer keeps the sanitizer defaults. */
const char *__asan_default_options(void) { return "detect_leaks=0"; }

static void json_string(const char *s) {
  putchar('"');
  for (; *s; ++s) {
    unsigned char c = (unsigned char)*s;
    if (c == '"' || c == '\\') printf("\\%c", c);
    else if (c < 0x20) printf("\\u%04x", c);
    else putchar(c);
  }
  putchar('"');
}

int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp4_result result;
 if(!parsarium_parse_mp4(data,n,&result))return 5;
 printf("{\"container\":");json_string(result.container);
 printf(",\"title\":");json_string(result.title);
 printf(",\"video_codec\":");json_string(result.video_codec);
 printf(",\"audio_codec\":");json_string(result.audio_codec);
 printf("}\n");
 return 0;
}
