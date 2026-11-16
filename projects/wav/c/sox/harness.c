#include "harness.h"
#include <sox.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int parsarium_parse_wav(const uint8_t*data,size_t size,struct parsarium_wav_result*result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 char path[]="/tmp/parsarium-sox-XXXXXX.wav";int fd=mkstemps(path,4);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}close(fd);
 if(sox_init()!=SOX_SUCCESS){unlink(path);return 0;}
 sox_format_t*file=sox_open_read(path,NULL,NULL,NULL);unlink(path);
 if(!file){sox_quit();return 0;}
 sox_sample_t raw[4]={0};size_t read=sox_read(file,raw,4);
 int ok=file->signal.channels==1&&(unsigned)file->signal.rate==8000&&read==4;
 if(ok){sox_uint64_t clips=0;SOX_SAMPLE_LOCALS;result->sample_rate=8000;result->channels=1;result->frames=file->signal.length;
  for(int i=0;i<4;i++)result->samples[i]=SOX_SAMPLE_TO_SIGNED_16BIT(raw[i],clips);}
 sox_close(file);sox_quit();return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t*data,size_t size){struct parsarium_wav_result r;(void)parsarium_parse_wav(data,size,&r);return 0;}
