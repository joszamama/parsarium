#define _POSIX_C_SOURCE 200809L
#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <libheif/heif.h>
#include <libheif/heif_sequences.h>
#define PARSARIUM_MAX_INPUT (1u<<20)
/* Same public sequence calls as adapters/c/mp4/libheif.c, on a local file path.
   libheif 1.23 treats isom/mp41/mp42 brands as sequences and parses moov/trak;
   tracks without a visual or metadata handler (audio) are skipped. The track
   count is libheif's, which may be zero; width and height are the first video
   track's. A libheif error fails the input; replay prints its message. */
static int fail(struct parsarium_mp4_result *result,heif_error error){
 snprintf(result->error,sizeof(result->error),"libheif error %d.%d: %s",
          (int)error.code,(int)error.subcode,error.message?error.message:"");
 return 0;
}
static int inspect(const char *path,struct parsarium_mp4_result *result){
 heif_context *context=heif_context_alloc();if(!context)return 0;
 heif_error error=heif_context_read_from_file(context,path,NULL);
 if(error.code!=heif_error_Ok){fail(result,error);heif_context_free(context);return 0;}
 int count=heif_context_number_of_sequence_tracks(context);
 int ok=count>=0;
 unsigned video=0,width=0,height=0;
 uint32_t *ids=count>0?malloc((size_t)count*sizeof(uint32_t)):NULL;
 if(count>0&&!ids)ok=0;
 if(ok&&count>0){
  heif_context_get_track_ids(context,ids);
  for(int i=0;ok&&i<count;i++){
   heif_track *track=heif_context_get_track(context,ids[i]);
   if(!track){ok=0;break;}
   if(heif_track_get_track_handler_type(track)==heif_track_type_video&&!video++){
    uint16_t w=0,h=0;
    error=heif_track_get_image_resolution(track,&w,&h);
    if(error.code==heif_error_Ok){width=w;height=h;}
    else ok=fail(result,error);
   }
   heif_track_release(track);
  }
 }
 free(ids);
 if(ok){result->sequence_tracks=(unsigned)count;result->video_tracks=video;result->width=width;result->height=height;}
 heif_context_free(context);
 return ok;
}
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result){
 if(!data||!result||!size||size>PARSARIUM_MAX_INPUT)return 0;
 result->error[0]=0;
 char path[]="/tmp/parsarium-mp4-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);int ok=inspect(path,result);
 unlink(path);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;(void)parsarium_parse_mp4(data,size,&result);return 0;
}
