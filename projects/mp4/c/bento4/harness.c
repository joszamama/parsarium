#define _POSIX_C_SOURCE 200809L
#include "harness.h"
#include <stdlib.h>
#include <unistd.h>
#include <Bento4C.h>
#define PARSARIUM_MAX_INPUT (1u<<20)
#define PARSARIUM_MAX_TRACKS 64u
static int reportable(unsigned char c){return c>=0x20&&c<0x7f&&c!='"'&&c!='\\';}
static int inspect(const char *path,struct parsarium_mp4_result *result){
 AP4_Result status=AP4_SUCCESS;
 AP4_ByteStream *stream=AP4_FileByteStream_Create(path,AP4_FILE_BYTE_STREAM_MODE_READ,&status);
 if(!stream||status!=AP4_SUCCESS)return 0;
 int ok=0;AP4_File *file=AP4_File_FromStream(stream,1);
 AP4_Movie *movie=file?AP4_File_GetMovie(file):NULL;AP4_UI32 brand=0;
 if(movie&&AP4_File_GetFileType(file,&brand,NULL,NULL)==AP4_SUCCESS){
  AP4_Cardinal tracks=AP4_Movie_GetTrackCount(movie);
  unsigned video=0,audio=0;ok=tracks<=PARSARIUM_MAX_TRACKS;
  for(AP4_Ordinal i=0;ok&&i<tracks;i++){
   AP4_Track *track=AP4_Movie_GetTrackByIndex(movie,i);
   if(!track){ok=0;break;}
   int type=AP4_Track_GetType(track);
   if(type==AP4_TRACK_TYPE_VIDEO)video++;
   if(type==AP4_TRACK_TYPE_AUDIO)audio++;
  }
  for(int i=0;ok&&i<4;i++){
   unsigned char c=(unsigned char)(brand>>(24-8*i));
   if(!reportable(c))ok=0;else result->brand[i]=(char)c;
  }
  if(ok){result->brand[4]=0;result->tracks=tracks;result->video_tracks=video;
   result->audio_tracks=audio;result->duration_ms=AP4_Movie_GetDurationMs(movie);}
 }
 if(file)AP4_File_Destroy(file);
 AP4_ByteStream_Release(stream);
 return ok;
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
