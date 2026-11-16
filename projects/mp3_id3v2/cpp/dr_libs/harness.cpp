#define DR_MP3_IMPLEMENTATION
#include <dr_mp3.h>
#include "harness.h"
#include <string.h>
struct tag_state { size_t id3v2_bytes; };
static void on_meta(void *ctx,const drmp3_metadata *meta) {
 struct tag_state *state=(struct tag_state *)ctx;
 if(meta->type==DRMP3_METADATA_TYPE_ID3V2) state->id3v2_bytes=meta->rawDataSize;
}
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result) {
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 struct tag_state state={0};drmp3 mp3;
 if(!drmp3_init_memory_with_metadata(&mp3,data,size,on_meta,&state,NULL))return 0;
 drmp3_int16 pcm[2]={0};
 drmp3_uint64 frames=drmp3_read_pcm_frames_s16(&mp3,1,pcm);
 result->sample_rate=mp3.sampleRate;result->channels=mp3.channels;
 result->decoded_frames=frames;result->id3v2_bytes=state.id3v2_bytes;
 drmp3_uninit(&mp3);
 return frames==1 && state.id3v2_bytes>0;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_mp3_result result;(void)parsarium_parse_mp3(data,size,&result);return 0;
}
