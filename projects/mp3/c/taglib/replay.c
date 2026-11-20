#include "harness.h"
#include <stdio.h>
/* Print s as a JSON string; bytes that are not UTF-8 are written as \u00XX. */
static void json_string(const char *s){
 const unsigned char *p=(const unsigned char *)s;putchar('"');
 while(*p){unsigned c=*p;int n=c<0x80?1:(c>>5)==6?2:(c>>4)==14?3:(c>>3)==30?4:0,valid=n>0;
  for(int i=1;i<n&&valid;i++)if((p[i]&0xC0)!=0x80)valid=0;
  if(!valid){printf("\\u%04x",c);p++;continue;}
  if(n>1){fwrite(p,1,(size_t)n,stdout);p+=n;continue;}
  if(c=='"'||c=='\\')printf("\\%c",c);else if(c<0x20)printf("\\u%04x",c);else putchar((int)c);p++;}
 putchar('"');
}
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp3_result result;
 if(!parsarium_parse_mp3(data,n,&result))return 5;
 printf("{\"title\":");json_string(result.title);printf(",\"artist\":");json_string(result.artist);printf("}\n");
 return 0;
}
