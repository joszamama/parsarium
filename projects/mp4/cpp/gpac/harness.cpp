#include "harness.h"
#include <cstdarg>
#include <cstdio>
#include <cstring>
#include <unistd.h>
#include <gpac/isomedia.h>
#define PARSARIUM_MAX_INPUT (1u<<20)
/* The selected call site is a CLI. Compile it here as C++17 with its entry point
   and stdout write renamed, and track the GF_ISOFile it opens so its early error
   returns cannot leak across fuzz iterations. GPAC calls and arguments are unchanged. */
static char adapter_output[sizeof(parsarium_mp4_result::json)];
static size_t adapter_output_len;
static bool adapter_output_overflow;
static GF_ISOFile *adapter_file;
__attribute__((format(printf,1,2)))
static int adapter_printf(const char *format,...){
 size_t room=sizeof(adapter_output)-adapter_output_len;
 va_list args;va_start(args,format);
 int n=vsnprintf(adapter_output+adapter_output_len,room,format,args);
 va_end(args);
 if(n<0||(size_t)n>=room){adapter_output_overflow=true;return n;}
 adapter_output_len+=(size_t)n;return n;
}
static GF_ISOFile *adapter_open(const char *name,GF_ISOOpenMode mode,const char *tmp_dir){
 adapter_file=gf_isom_open(name,mode,tmp_dir);return adapter_file;
}
static void adapter_delete(GF_ISOFile *file){
 if(file==adapter_file)adapter_file=NULL;
 gf_isom_delete(file);
}
#define main parsarium_gpac_adapter_main
#define printf adapter_printf
#define gf_isom_open adapter_open
#define gf_isom_delete adapter_delete
#include "adapter/cpp/mp4/gpac.cpp"
#undef gf_isom_delete
#undef gf_isom_open
#undef printf
#undef main
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result){
 if(!data||!result||!size||size>PARSARIUM_MAX_INPUT)return 0;
 char path[]="/tmp/parsarium-mp4-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);
 adapter_output[0]=0;adapter_output_len=0;adapter_output_overflow=false;adapter_file=NULL;
 char arg0[]="gpac";char *argv[]={arg0,path,NULL};
 int status=parsarium_gpac_adapter_main(2,argv);
 if(adapter_file){gf_isom_delete(adapter_file);adapter_file=NULL;}
 unlink(path);
 if(status!=0||adapter_output_overflow||!adapter_output_len)return 0;
 memcpy(result->json,adapter_output,adapter_output_len+1);return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;(void)parsarium_parse_mp4(data,size,&result);return 0;
}
