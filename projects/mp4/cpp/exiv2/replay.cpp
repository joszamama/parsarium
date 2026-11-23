#include "harness.h"
#include <stdio.h>
#include <string>
static void print_json_string(const std::string &text){
 putchar('"');
 for(unsigned char c:text){
  if(c=='"'||c=='\\'){putchar('\\');putchar(c);}
  else if(c<0x20)printf("\\u%04x",c);
  else putchar(c);
 }
 putchar('"');
}
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp4_result result;
 if(!parsarium_parse_mp4(data,n,&result)){fprintf(stderr,"%s\n",result.error.c_str());return 5;}
 // Fields Exiv2 did not record for this file are left out.
 const char *sep="";putchar('{');
 if(result.has_brand){printf("\"brand\":");print_json_string(result.brand);sep=",";}
 if(result.has_width){printf("%s\"width\":%ld",sep,result.width);sep=",";}
 if(result.has_height){printf("%s\"height\":%ld",sep,result.height);sep=",";}
 printf("}\n");
 return 0;
}
