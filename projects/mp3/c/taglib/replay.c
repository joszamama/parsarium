#include "harness.h"
#include <stdio.h>
int main(int argc,char **argv){
 if(argc!=2)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);
 if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}
 fclose(f);struct parsarium_mp3_result result;
 if(!parsarium_parse_mp3(data,n,&result))return 5;
 printf("{\"title\":\"%s\",\"artist\":\"%s\"}\n",result.title,result.artist);
 return 0;
}
