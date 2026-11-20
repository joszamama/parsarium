#include "harness.h"
#include <SDL.h>
#include <SDL_mixer.h>
#include <string.h>

int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  SDL_setenv("SDL_AUDIODRIVER", "dummy", 1);
  if (SDL_Init(SDL_INIT_AUDIO) != 0) return 0;
  if (!(Mix_Init(MIX_INIT_MP3) & MIX_INIT_MP3)) { SDL_Quit(); return 0; }
  if (Mix_OpenAudio(8000,AUDIO_S16LSB,1,1024) != 0) { Mix_Quit(); SDL_Quit(); return 0; }
  SDL_RWops *input=SDL_RWFromConstMem(data,(int)size);
  if (!input) { Mix_CloseAudio(); Mix_Quit(); SDL_Quit(); return 0; }
  Mix_Music *music=Mix_LoadMUSType_RW(input,MUS_MP3,1);
  if (!music) { Mix_CloseAudio(); Mix_Quit(); SDL_Quit(); return 0; }
  const char *title=Mix_GetMusicTitleTag(music), *artist=Mix_GetMusicArtistTag(music);
  double seconds=Mix_MusicDuration(music);
  int ok=Mix_GetMusicType(music)==MUS_MP3 && title && artist &&
         strlen(title)<sizeof(result->title) && strlen(artist)<sizeof(result->artist) && seconds>=0;
  if (ok) {
    memcpy(result->title,title,strlen(title)+1); memcpy(result->artist,artist,strlen(artist)+1);
    result->duration_ms=(int)(seconds*1000.0+0.5);
  }
  Mix_FreeMusic(music); Mix_CloseAudio(); Mix_Quit(); SDL_Quit();
  return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
  struct parsarium_mp3_result result;
  (void)parsarium_parse_mp3(data,size,&result);
  return 0;
}
