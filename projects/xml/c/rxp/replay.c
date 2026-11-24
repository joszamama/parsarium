#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char **argv){if(argc!=2)return 2;FILE*f=fopen(argv[1],"rb");if(!f)return 3;static uint8_t data[1u<<20];size_t n=fread(data,1,sizeof(data),f);if(ferror(f)||(n==sizeof(data)&&fgetc(f)!=EOF)){fclose(f);return 4;}fclose(f);char*out=parsarium_parse_xml(data,n);if(!out){const char*e=parsarium_xml_error();if(*e)fprintf(stderr,"%s\n",e);return 5;}printf("%s\n",out);free(out);return 0;}
