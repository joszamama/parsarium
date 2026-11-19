#include "harness.h"
#include <memory>
#include <vector>
#include <cstdio>
#include <stdlib.h>
#include <unistd.h>
#include <libheif/heif.h>
#include <libheif/heif_sequences.h>
// Same public sequence calls as adapters/cpp/mp4/libheif.cpp, on a local file path,
// with RAII ownership of the context and tracks. libheif 1.23 treats isom/mp41/mp42
// brands as sequences and parses moov/trak; audio tracks are skipped by this API.
// The track count is libheif's and may be zero; width and height are the first
// video track's. A libheif error fails the input; replay prints its message.
namespace {
constexpr size_t max_input=1u<<20;
struct context_free { void operator()(heif_context *c) const { heif_context_free(c); } };
struct track_release { void operator()(heif_track *t) const { heif_track_release(t); } };
using context_ptr=std::unique_ptr<heif_context,context_free>;
using track_ptr=std::unique_ptr<heif_track,track_release>;

bool fail(parsarium_mp4_result &result,const heif_error &error){
 std::snprintf(result.error,sizeof(result.error),"libheif error %d.%d: %s",
               static_cast<int>(error.code),static_cast<int>(error.subcode),error.message?error.message:"");
 return false;
}

bool inspect(const char *path,parsarium_mp4_result &result){
 context_ptr context(heif_context_alloc());
 if(!context)return false;
 heif_error error=heif_context_read_from_file(context.get(),path,nullptr);
 if(error.code!=heif_error_Ok)return fail(result,error);
 const int count=heif_context_number_of_sequence_tracks(context.get());
 if(count<0)return false;
 std::vector<uint32_t> ids(static_cast<size_t>(count));
 if(count)heif_context_get_track_ids(context.get(),ids.data());
 unsigned video=0;uint16_t width=0,height=0;
 for(uint32_t id:ids){
  track_ptr track(heif_context_get_track(context.get(),id));
  if(!track)return false;
  if(heif_track_get_track_handler_type(track.get())!=heif_track_type_video)continue;
  if(video++)continue;
  error=heif_track_get_image_resolution(track.get(),&width,&height);
  if(error.code!=heif_error_Ok)return fail(result,error);
 }
 result.sequence_tracks=static_cast<unsigned>(count);result.video_tracks=video;
 result.width=width;result.height=height;
 return true;
}

struct temp_file {
 char path[32]="/tmp/parsarium-mp4-XXXXXX";
 int fd=mkstemp(path);
 bool created=fd>=0;
 ~temp_file(){ if(fd>=0)close(fd); if(created)unlink(path); }
};
}

int parsarium_parse_mp4(const uint8_t *data,size_t size,parsarium_mp4_result *result){
 if(!data||!result||!size||size>max_input)return 0;
 result->error[0]=0;
 temp_file file;if(file.fd<0)return 0;
 for(size_t off=0;off<size;){
  ssize_t n=write(file.fd,data+off,size-off);
  if(n<=0)return 0;
  off+=static_cast<size_t>(n);
 }
 close(file.fd);file.fd=-1;
 bool ok=inspect(file.path,*result);
 return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 parsarium_mp4_result result;(void)parsarium_parse_mp4(data,size,&result);return 0;
}
