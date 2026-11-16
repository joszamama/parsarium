#include "harness.h"
#include <SDL3/SDL.h>
#include <SDL3_mixer/SDL_mixer.h>
#include <string.h>

int parsarium_parse_wav(const uint8_t *data,size_t size,struct parsarium_wav_result *result) {
 if(!data||!result||!size||size>(1u<<20)) return 0;
 memset(result,0,sizeof(*result));
 if(!MIX_Init()) return 0;
 SDL_IOStream *input=SDL_IOFromConstMem(data,size);
 if(!input){MIX_Quit();return 0;}
 MIX_Audio *audio=MIX_LoadAudio_IO(NULL,input,true,true);
 if(!audio){MIX_Quit();return 0;}
 SDL_AudioSpec spec;
 Sint64 frames=MIX_GetAudioDuration(audio);
 int ok=MIX_GetAudioFormat(audio,&spec)&&spec.freq==8000&&spec.channels==1&&frames==4;
 if(ok){result->sample_rate=spec.freq;result->channels=spec.channels;result->frames=frames;}
 MIX_DestroyAudio(audio);MIX_Quit();return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_wav_result result;(void)parsarium_parse_wav(data,size,&result);return 0;
}
