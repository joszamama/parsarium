#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (SDL_setenv("SDL_AUDIODRIVER", "dummy", 1) != 0) return 1;
  if ((Mix_Init(MIX_INIT_MP3) & MIX_INIT_MP3) == 0) return 1;
  if (Mix_OpenAudio(8000, AUDIO_S16SYS, 1, 1024) != 0) return 1;
  Mix_Music *music = Mix_LoadMUS(argv[1]);
  if (!music || Mix_GetMusicType(music) != MUS_MP3) return 1;
  const char *title = Mix_GetMusicTitleTag(music);
  const char *artist = Mix_GetMusicArtistTag(music);
  double seconds = Mix_MusicDuration(music);
  if (!title || !*title || !artist || !*artist || seconds <= 0) return 1;
  printf("{\"title\":\"%s\",\"artist\":\"%s\",\"duration_ms\":%d}\n",
         title, artist, (int)(seconds * 1000.0 + 0.5));
  Mix_FreeMusic(music);
  Mix_CloseAudio();
  Mix_Quit();
  return 0;
}
