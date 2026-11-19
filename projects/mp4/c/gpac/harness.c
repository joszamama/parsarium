#define _POSIX_C_SOURCE 200809L
#include "harness.h"
#include <stdlib.h>
#include <limits.h>
#include <unistd.h>
#include <gpac/isomedia.h>
#define PARSARIUM_MAX_INPUT (1u<<20)
/* Same public ISO media calls as adapters/c/mp4/gpac.c, on a local file path.
   width and height are the first visual track's sample description size and
   duration_ms needs a movie timescale; each is unset when the file has none. */
static int inspect(const char *path,struct parsarium_mp4_result *result){
 GF_ISOFile *file=gf_isom_open(path,GF_ISOM_OPEN_READ,NULL);
 if(!file)return 0;
 u32 tracks=gf_isom_get_track_count(file);
 u32 video=0,audio=0,width=0,height=0;int has_size=0;
 for(u32 i=1;i<=tracks;i++){
  u32 type=gf_isom_get_media_type(file,i);
  if(type==GF_ISOM_MEDIA_VISUAL){
   if(!video++){
    u32 sample_width=0,sample_height=0;
    if(gf_isom_get_visual_info(file,i,1,&sample_width,&sample_height)==GF_OK){
     width=sample_width;height=sample_height;has_size=1;
    }
   }
  }else if(type==GF_ISOM_MEDIA_AUDIO)audio++;
 }
 u32 timescale=gf_isom_get_timescale(file);
 u64 duration=gf_isom_get_duration(file);
 result->tracks=tracks;result->video_tracks=video;result->audio_tracks=audio;
 result->has_size=has_size;result->width=width;result->height=height;
 result->has_duration=timescale!=0;
 __uint128_t milliseconds=timescale ? (__uint128_t)duration*1000/timescale : 0;
 result->duration_ms=milliseconds>ULLONG_MAX ? ULLONG_MAX : (unsigned long long)milliseconds;
 gf_isom_delete(file);
 return 1;
}
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result){
 if(!data||!result||!size||size>PARSARIUM_MAX_INPUT)return 0;
 char path[]="/tmp/parsarium-mp4-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);int ok=inspect(path,result);
 unlink(path);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;(void)parsarium_parse_mp4(data,size,&result);return 0;
}
