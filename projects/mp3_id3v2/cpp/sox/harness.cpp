#include "harness.h"
#include <sox.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int parsarium_parse_mp3(const uint8_t*data,size_t size,struct parsarium_mp3_result*result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 char path[]="/tmp/parsarium-sox-XXXXXX.mp3";int fd=mkstemps(path,4);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}close(fd);
 if(sox_init()!=SOX_SUCCESS){unlink(path);return 0;}
 sox_format_t*file=sox_open_read(path,NULL,NULL,NULL);unlink(path);
 if(!file){sox_quit();return 0;}
 sox_sample_t sample=0;size_t decoded=sox_read(file,&sample,1);
 int ok=file->filetype&&strcmp(file->filetype,"mp3")==0&&decoded==1&&strlen(file->filetype)<sizeof(result->filetype);
 if(ok){strcpy(result->filetype,file->filetype);result->sample_rate=(unsigned)file->signal.rate;result->channels=file->signal.channels;result->decoded_samples=decoded;}
 sox_close(file);sox_quit();return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t*data,size_t size){struct parsarium_mp3_result r;(void)parsarium_parse_mp3(data,size,&r);return 0;}
